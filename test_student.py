import unittest
from proj1 import *
#proj1.py should contain your data class and function definitions
#these do not contribute positivly to your grade. 
#but your grade will be lowered if they are missing

class TestRegionFunctions(unittest.TestCase):

    def setUp(self):
        self.rect = GlobeRect(lo_lat=10.0, hi_lat=20.0, west_long=30.0, east_long=40.0)
        self.region = Region(rect=self.rect, name="Testland", terrain="other")
        self.regionregion = Region(rect=self.rect, name="Testy", terrain="other")
        self.rc = RegionCondition(region=self.region, year=2025, pop=1000, ghg_rate=5000.0)
        self.rcc = RegionCondition(region=self.regionregion, year=2025, pop=1500, ghg_rate=5000.0)
        self.newrc = RegionCondition(region=self.region, year=2026, pop=1000, ghg_rate=5000)
        self.blank = []
      
      #wl -l1 - 0.52359 
        # el -l2 - 0.6981 
        # ll - t1 - 0.1745329 
        # hl-t2 - 0.349065 
        #area - 1195283.024
        #em per sq km - 0.00418

    #emission_per_cap_test
    def test_reg_epc(self):
        result = emissions_per_capita(self.rc)
        self.assertAlmostEqual(result,5.0, places=2)

    #test area
    def test_reg_area(self):
        result = area(self.rect)
        self.assertAlmostEqual(result,1195445.545, places=2)

    #test emissions per sq km
    def test_reg_epsk(self):
        result = emissions_per_square_km(self.rc)
        self.assertAlmostEqual(result, 0.00418, places=5)

    #test densest
    def test_densest(self):
        result = densest([self.rc,self.rcc])
        self.assertEqual(result, "Testy")

    #test for projected conditions
    
    def test_proj_cond(self):
        result = project_condition(self.rc, 1)
        self.assertEqual(result, self.newrc)

    def test_dense_empty(self):
        self.assertRaises(ValueError, densest,[])


if __name__ == '__main__':
    unittest.main()
