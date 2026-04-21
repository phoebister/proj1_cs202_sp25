#complete your tasks in this file
import sys
import unittest
import math
from typing import *
from dataclasses import dataclass

sys.setrecursionlimit(10**6)

#follow design recipe
'''
purpose statement:
calculates emissions per capita, area, emissions per square km, and identifies the
highest population density from a group of regions, and also predicts a regions population growth
after a give number of years
'''

#data definitions

@dataclass (frozen=True)
class GlobeRect:
    lo_lat:float
    hi_lat:float
    west_long:float
    east_long:float

@dataclass (frozen=True)
class Region:
    rect: GlobeRect
    name: str
    terrain: str #can only be ocean, mountains, forest, or other

@dataclass (frozen=True)
class RegionCondition:
    region: Region
    year: int
    pop: int
    ghg_rate: float

#task 2 create example data

la_gr = GlobeRect(
    lo_lat = 33.7,
    hi_lat = 34.8,
    west_long = -118.9,
    east_long = -117.6
) #N and W

nsw_gr = GlobeRect(
    lo_lat = -38.0,
    hi_lat = -28.0,
    west_long = 141.0,
    east_long = 154.0
) #S and E

slo_gr = GlobeRect(
    lo_lat = 34.54,
    hi_lat = 35.48,
    west_long = -121.02,
    east_long = -119.27
) #N and W

tac_gr = GlobeRect(
    lo_lat = 20.0,
    hi_lat = 22.5,
    west_long = -72.5,
    east_long = -70.0
)

# region's now

la_reg = Region(
    rect = la_gr,
    name = "Los Angeles County",
    terrain = "other"
)

nsw_reg = Region(
    rect = nsw_gr,
    name = "New South Wales",
    terrain = "mountains"
)

slo_reg = Region(
    rect = slo_gr,
    name = "San Luis Obispo County",
    terrain = "mountains"
)

tac_reg = Region(
    rect = tac_gr,
    name = "Turks and Caicos",
    terrain = "ocean"
)

#condition list now

region_conditions = [
    RegionCondition(
        region= la_reg,
        year= 2025,
        pop= 9700000,
        ghg_rate= 360400000
    ),

    RegionCondition(
        region= nsw_reg,
        year= 2018,
        pop= 8000000,
        ghg_rate= 143500000
    ),

    RegionCondition(
        region= slo_reg,
        year= 2025,
        pop= 282440,
        ghg_rate= 150600
    ),

    RegionCondition(
        region = tac_reg,
        year = 2020,
        pop = 44300,
        ghg_rate = 359000
    )
]


#okay code now

def emissions_per_capita(rc: RegionCondition)->float:
    if rc.pop == 0:
        return 0.0
    em_per_cap = rc.ghg_rate/rc.pop
    return round(em_per_cap,2)

def area(gr: GlobeRect) -> float:
    #don't forget when they cross the equator - figure that out
    t1 = math.radians(gr.lo_lat)
    t2 = math.radians(gr.hi_lat)
    l1 = math.radians(gr.west_long)
    l2 = math.radians(gr.east_long)
    long_dist = l2-l1
    if long_dist <0:
        long_dist = long_dist+2*math.pi

    a = (6378.1**2)*long_dist*abs(math.sin(t2)-math.sin(t1))
    return a

def emissions_per_square_km(rc: RegionCondition) -> float:
    em_per_sqkm = rc.ghg_rate/area(rc.region.rect)
    if area(rc.region.rect) == 0:
        return 0.0
    return em_per_sqkm
 

#helper fn for density
def dense_helper(rc_list, idx: int) -> RegionCondition:
    if len(rc_list) == 1:
        return rc_list[0]
    
    if idx == len(rc_list)-1:
        return rc_list[idx]
    den = dense_helper(rc_list, idx+1)

    current_density = rc_list[idx].pop / area(rc_list[idx].region.rect)
    den_density = den.pop/ area(den.region.rect)
    if current_density > den_density:
        return rc_list[idx]
    else: 
        return den
def densest(rc_list: list[RegionCondition]) -> str:
    if len(rc_list) == 0:
        raise ValueError("list can't be empty")
    dense = dense_helper(rc_list,0)
    return dense.region.name
#must be recursive, no while, min, max
    

def helper_pop_grow(pop:int, rate: float, years: int) -> int:
    new_pop = pop*(1+rate)**years
    return int(round(new_pop,0))

def helper_emissions(pop:int,np: int, ghg_em:float)->float:
    new_em = ghg_em*(np/pop)
    return new_em

#projected condition time
def project_condition(rc: RegionCondition, years: int) -> RegionCondition:
    if years < 0:
        raise ValueError("years must be non-negative")
    elif rc.region.terrain == "ocean":
        rate = 0.0001
    elif rc.region.terrain =="mountains":
        rate = 0.0005
    elif rc.region.terrain == "forest":
        rate = -0.00001
    elif rc.region.terrain == "other":
        rate = 0.0003
    new_population = helper_pop_grow(rc.pop,rate, years)
    new_emissions = helper_emissions(rc.pop, new_population,rc.ghg_rate)
    projected = RegionCondition(rc.region,rc.year+years,new_population,new_emissions)
    return projected