from sys_info_mqtt import get_system_info
import unittest

class Test_Sys_Info_Mqtt(unittest.TestCase):

    def test_get_system_info(self):
        test_loadavg_keys = ['loadavg1', 'loadavg5', 'loadavg15', 
                    'loadavg1percent', 'loadavg5percent', 'loadavg15percent']
        test_os_cpucount = 1
        
        test_os_loadavg = list((0.19, 0.16, 0.15))
        test_loadavg_percent_vals = [19.0, 16.0, 15.0]
        test_os_loadavg.extend(test_loadavg_percent_vals)

        test_dict = { 
            'myhost': {
                'cpu': {
                    'count': test_os_cpucount,
                    'loadavg': dict(zip(test_loadavg_keys, test_os_loadavg))
                }
            }
        }

        print(test_dict)
        print(get_system_info("myhost", 1, test_os_loadavg))
        
        info_dict = get_system_info("myhost", 1, test_os_loadavg)
        self.assertDictEqual(test_dict, info_dict)

        test_os_loadavg = (0.19, 0.16, 0.15)
        info_dict = get_system_info("myhost", 0, test_os_loadavg)
        self.assertDictEqual(test_dict, info_dict)
        


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)