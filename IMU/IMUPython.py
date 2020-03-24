from ctypes import *
import sys
import time
import math
rs = CDLL('./rs232.so')
spatial = CDLL('./spatial_packets.so')
packets = CDLL('./an_packet_protocol.so')

######### defines & macros #################
AN_PACKET_HEADER_SIZE = 5
AN_MAXIMUM_PACKET_SIZE =  255
AN_DECODE_BUFFER_SIZE = 10*(AN_MAXIMUM_PACKET_SIZE+AN_PACKET_HEADER_SIZE)
RADIANS_TO_DEGREES = 180.0/math.pi
accelerometer_range_4g = 1
gyroscope_range_500dps = 1
magnetometer_range_2g = 0

packet_id_system_state = 20
########## structs ##########################
class an_packet_t(Structure):
    _fields_ = [("id", c_uint8),
                ("length", c_uint8),
                ("header", c_uint8*AN_PACKET_HEADER_SIZE),
                ("data", c_void_p)]


class an_decoder_t(Structure):
    _fields_ = [("buffer", c_uint8 * AN_DECODE_BUFFER_SIZE),
                ("buffer_length", c_uint16),
                ("crc_errors", c_uint)]

class sensor_ranges_packet_t(Structure):
	_fields_ = [("permanent",c_uint8),
                ("accelerometers_range",c_uint8),
                ("gyroscopes_range", c_uint8),
                ("magnetometers_range",c_uint8)]


# class b(Structure):
# 			unsigned int orientation_filter_initialised :1; 1
# 			unsigned int ins_filter_initialised :1;2
# 			unsigned int heading_initialised :1;3
# 			unsigned int utc_time_initialised :1;4
# 			unsigned int gnss_fix_type :3;5,6,7
# 			unsigned int event1_flag :1;8
# 			unsigned int event2_flag :1;9
# 			unsigned int internal_gnss_enabled :1;10
# 			unsigned int magnetic_heading_enabled :1;11
# 			unsigned int velocity_heading_enabled :1;12
# 			unsigned int atmospheric_altitude_enabled :1;13
# 			unsigned int external_position_active :1;14
# 			unsigned int external_velocity_active :1;15
# 			unsigned int external_heading_active :1;16

class system_state_packet_t(Structure):
    _fields_ = [("system_status",c_uint16),
                ("filter_status",c_uint16),
                ("unix_time_seconds", c_uint32),
                ("microseconds", c_uint32),
                ("latitude", c_double),
                ("longitude",c_double),
                ("height",c_double),
                ("velocity",3*c_float),
                ("body_acceleration",3*c_float),
                ("g_force",c_float),
                ("orientation",3*c_float),
                ("angular_velocity",3*c_float),
                ("standard_deviation",3*c_float)]


packets.an_packet_decode.restype = POINTER(an_packet_t)
spatial.encode_sensor_ranges_packet.restype = POINTER(an_packet_t)
############# costants %%%%%%%%%%%%%%%%%%%%%%%%
comPort = "COM3"
# comPort = "/dev/ttyUSB0" #nvidia's comport


########### auxilary functions #############

def  an_packet_transmit(an_packet):
    packets.an_packet_encode(byref(an_packet))
    return rs.SendBuf(packets.an_packet_pointer(byref(an_packet)), packets.an_packet_size(byref(an_packet)))

def set_sensor_ranges():

	sensor_ranges_packet = sensor_ranges_packet_t()
	sensor_ranges_packet.permanent = True
	sensor_ranges_packet.accelerometers_range = accelerometer_range_4g
	sensor_ranges_packet.gyroscopes_range = gyroscope_range_500dps
	sensor_ranges_packet.magnetometers_range = magnetometer_range_2g

	an_packet = spatial.encode_sensor_ranges_packet(byref(sensor_ranges_packet))
	an_packet_transmit(an_packet)

	# an_packet_free(&an_packet)


########### main functions ################
def ImuLoop():
    an_decoder = an_decoder_t()
    an_packet = an_packet_t()
    system_state_packet = system_state_packet_t()

    if(rs.OpenComport(create_string_buffer(comPort.encode('utf-8')),115200)==0):
        print('opend comport sucssesfuly')

    else:
        print ('faile to open comport')
        # exit(0)

    packets.an_decoder_initialise(byref(an_decoder))

    ############# Get a GPS FIX ###############
    ############# To Do: this funtion still dosent work problam is filter_status alwaya = 0 #################
    # No_fix = True
    # while No_fix == True:
    #     pointer = packets.an_decoder_pointer(byref(an_decoder))
    #     size = packets.an_decoder_size(byref(an_decoder))
    #     bytes_received = rs.PollComport(pointer,size)
    #     if bytes_received>0:
    #         packets.an_decoder_increment(byref(an_decoder),bytes_received)

    #         an_packet = packets.an_packet_decode(byref(an_decoder))
    #         while an_packet:
    #             if an_packet.contents.id == packet_id_system_state:    
    #                 res = spatial.decode_system_state_packet(byref(system_state_packet),an_packet)
    #                 if(res == 0):
    #                     #printf("No fix yet:\n");
    #                     if system_state_packet.filter_status !=0:
    #                         print ('someting in filter status')
    #                     # if system_state_packet.filter_status & 112 == 32:
    #                     #     No_fix = False
    #                     #     print("GNSS FIX STATUS: %d\n", system_state_packet.filter_status.b.gnss_fix_type)
    #                     # an_packet_free(&an_packet)        
    #             an_packet = packets.an_packet_decode(byref(an_decoder))
            
        
        



    while 1:
        pointer = packets.an_decoder_pointer(byref(an_decoder))
        size = packets.an_decoder_size(byref(an_decoder))
        bytes_received = rs.PollComport(pointer,size)
        if bytes_received>0:
            packets.an_decoder_increment(byref(an_decoder),bytes_received)
            an_packet = packets.an_packet_decode(byref(an_decoder))
            id = an_packet.contents.id
            if id == 20 :
                res = spatial.decode_system_state_packet(byref(system_state_packet),an_packet)
                if(res == 0):
                    print("Roll = {0}, Pitch = {1}, Heading = {2}\n".format(system_state_packet.orientation[0] * RADIANS_TO_DEGREES, system_state_packet.orientation[1] * RADIANS_TO_DEGREES, system_state_packet.orientation[2] * RADIANS_TO_DEGREES))
    rs.CloseComport()

