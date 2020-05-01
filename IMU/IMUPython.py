from ctypes import *
from Car import *
import csv
import sys
import time
import math
rs = CDLL('./IMU/rs232.so')
spatial = CDLL('./IMU/spatial_packets.so')
packets = CDLL('./IMU/an_packet_protocol.so')

######### defines & macros #################
AN_PACKET_HEADER_SIZE = 5
AN_MAXIMUM_PACKET_SIZE =  255
AN_DECODE_BUFFER_SIZE = 10*(AN_MAXIMUM_PACKET_SIZE+AN_PACKET_HEADER_SIZE)
RADIANS_TO_DEGREES = 180.0/math.pi
accelerometer_range_4g = 1
gyroscope_range_500dps = 1
magnetometer_range_2g = 0
MAXIMUM_PACKET_PERIODS = 50
packet_id_utm_position = 34
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

class utm_position_packet_t(Structure):
	_fields_ = [("position",c_double*3),
                ("zone",c_char)]

class packet_period_t(Structure):
    _fields_ = [('packet_id',c_uint8),
                ('period',c_uint32)]

class packet_periods_packet_t(Structure):
    _fields_ = [('permanent',c_uint8),
                ('clear_existing_packets',c_uint8),
                ('packet_periods', packet_period_t*MAXIMUM_PACKET_PERIODS)]

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
spatial.encode_packet_periods_packet.restype = POINTER(an_packet_t)
# spatial.decode_utm_position_packet.restype = c_int


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

def set_utm_packet_rate():
    utm_rate_packet = packet_periods_packet_t()
    utm_rate_packet.clear_existing_packets = 0
    utm_rate_packet.packet_periods[0].packet_id = packet_id_utm_position
    utm_rate_packet.packet_periods[0].period = 1

    an_packet = spatial.encode_packet_periods_packet(byref(utm_rate_packet))
    an_packet_transmit(an_packet)

    # an_packet_free(&an_packet)


########### main functions ################
def ImuLoop(q, plottingFileName,fieldnames):
    an_decoder = an_decoder_t()
    an_packet = an_packet_t()
    system_state_packet = system_state_packet_t()
    utm_position_packet = utm_position_packet_t()

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
    #             an_packet = packets.an_pac
    
    null_ptr = POINTER(c_int)()
        # set_utm_packet_rate()
    while 1:
        pointer = packets.an_decoder_pointer(byref(an_decoder))
        size = packets.an_decoder_size(byref(an_decoder))
        bytes_received = rs.PollComport(pointer,size)
        if bytes_received>0:
            packets.an_decoder_increment(byref(an_decoder),bytes_received)
            an_packet = packets.an_packet_decode(byref(an_decoder))

            if an_packet:
                id = an_packet.contents.id
                if id == 20 :
                    res = spatial.decode_system_state_packet(byref(system_state_packet),an_packet)
                    if(res == 0):
                        # print("Roll = {0}, Pitch = {1}, Heading = {2}\n".format(system_state_packet.orientation[0] * RADIANS_TO_DEGREES, system_state_packet.orientation[1] * RADIANS_TO_DEGREES, system_state_packet.orientation[2] * RADIANS_TO_DEGREES))
                        # q.put("Roll = {0}, Pitch = {1}, Heading = {2}\n".format(system_state_packet.orientation[0] * RADIANS_TO_DEGREES, system_state_packet.orientation[1] * RADIANS_TO_DEGREES, system_state_packet.orientation[2] * RADIANS_TO_DEGREES))
                        q.put(CarStatus(heading = system_state_packet.orientation[2] * RADIANS_TO_DEGREES ,uptadeType = 2))
                elif id == packet_id_utm_position:
                    
                    res = spatial.decode_utm_position_packet(byref(utm_position_packet),an_packet)
                    if(res == 0):

                        x = utm_position_packet.position[0]
                        y = utm_position_packet.position[1]
                        z = utm_position_packet.position[2] 
                        q.put(CarStatus(x,y,z,uptadeType = 1))



    rs.CloseComport()

