# -*- coding: utf-8 -*-
import unittest
import ose

class TestStringMethods(unittest.TestCase):

  def test_convert_seconds(self):
      self.assertEqual(ose.convertSecs(59), "0:59 mins")
      self.assertEqual(ose.convertSecs(60), "1:00 mins")
      self.assertEqual(ose.convertSecs(0), "0:00 mins")
      self.assertEqual(ose.convertSecs(120), "2:00 mins")
      self.assertEqual(ose.convertSecs(152), "2:32 mins")
  
  def test_get_station(self):
      self.assertEqual(ose.getStation(u'ΠΠΕΝ'), "Pentelis")
      self.assertEqual(ose.getStation(u'NON_EXISTING'), "NON_EXISTING")
  
  def test_get_next_station(self):
      self.assertEqual(ose.getNextStation(u'ΠΠΕΝ',"1",1), "Kifisias")
      self.assertEqual(ose.getNextStation(u'ΠΠΕΝ',"0",1), "")
      self.assertEqual(ose.getNextStation(u'ΠΠΕΝ',"1",2), "Doukisis")
      self.assertEqual(ose.getNextStation(u'ΠΠΕΝ',"0",2), "")
      self.assertEqual(ose.getNextStation(u'ΠΠΕΝ',"100.1",2), "Doukisis")
      self.assertEqual(ose.getNextStation(u'ΠΠΕΝ',"110.1",2), "Doukisis")
      self.assertEqual(ose.getNextStation(u'NON_EXISTING', "1",1), "")
      self.assertEqual(ose.getNextStation(u'NON_EXISTING', "1",2), "")
      self.assertEqual(ose.getNextStation(u'NON_EXISTING', "0",1), "")
      self.assertEqual(ose.getNextStation(u'NON_EXISTING', "0",2), "")


  def test_calculate_distance(self):
    self.assertEqual(round(ose.distance_on_unit_sphere(38.03303, 23.82242, 38.0418933333, 23.80414),2),1.88)
    self.assertEqual(round(ose.distance_on_unit_sphere(38.0418933333, 23.80414, 38.03303, 23.82242),2),1.88)
    self.assertEqual(round(ose.distance_from_station(38.0573183333, 23.7708183333,u"ΠΗΡΑ"),2), 0.11)

if __name__ == '__main__':
    unittest.main()
