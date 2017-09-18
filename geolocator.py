#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Script for geolocating adresses
#This script uses intensivly geocoder

import numpy as np
import geocoder


class Geolocator:

	#Initializer	
	def __init__(self, engines = ['google']):
		'''
		Parameters
		-----------------------------
		engines : array of Strings
			Array of the engines that geocoder will use. Can be any of the following:
			- arcgis (free)
			- google (request limit)
			- bing (api-key)
			- Yahoo
		-----------------------------
		'''

		#Saves engines	
		self.engines = np.array(engines)

		#Default location (North Pole Bitches!)
		self.defult_location = np.array([90,180])



	def get_error(self, coordinates_dic):
		'''
		Description
		Gets the error of a given set of coordinates. The error corresponds to the diagonal of
		the samallest enclosing square
		-----------------------------
		Parameters
		-----------------------------
		coordinates_dic : dictionary
			A dictinoary with lattitude and longitud values for each engine
		-----------------------------
		Return
		error : float
			An average error of the locations (assuming they all refer to the same location)
		'''
		#Earth radius in meters
		r = 6371000

		#Apply the haversine formula for the distance traveled by sequentially following the terms
		#https://en.wikipedia.org/wiki/Great-circle_distance

		#Calcultaes the square
		c = np.array(list(coordinates_dic.values()))
		x = np.amin(c, axis = 0)
		y = np.amax(c, axis = 0)
		
		#Absolute angle distance		
		delta = np.abs(x - y)

		#Haversine formula for low float point precision systems
		sigma = np.sin((delta[0])/2)**2 + np.cos(x[0])*np.cos(y[0])*np.sin((delta[1])/2)**2
		sigma = 2*np.arcsin(sigma)

		return(r*np.sum(sigma))



	def get_coordinates(self, address, city = 'Bogota', country = 'Colombia'):
		'''
		Parameters
		-----------------------------
		coordinates : numpy array
			A numpy array of shape (N,2) with N lat, long coordinates of a same address 
		-----------------------------
		Return
		error : float
			An average error of the locations (assuming they all refer to the same location)
		'''

		complete_location = address + ',' + city + ',' +  country

		eng = np.reshape(self.engines, (len(self.engines),1))

		latlng = np.apply_along_axis(lambda x: self.process_request(complete_location,x[0]),1, eng)

		return(dict(zip(self.engines, latlng)))



	def process_request(self, complete_location, geo_engine):
		'''
		Description
		Gets the lattitude and longitud of a complete location, given an specific search engine
		-----------------------------
		Parameters
		-----------------------------
		complete_location : String
			locations complete adress (including city and country)
		geo_engine : String
			String that geocoder will use. Can be any of the following:
			- arcgis (free)
			- google (request limit)
			- bing (api-key) 	
			- Yahho	
		-----------------------------
		Return
		coordinates : numpy array
			Two dimensional array with the lattitude and longitud (in that order)
		'''	
		try:
			#Google
			if(geo_engine.lower() == 'google'):
				 g = geocoder.google(complete_location)		 
			#Argis
			elif(geo_engine.lower() == 'arcgis'):
				g = geocoder.arcgis(complete_location)
			#Argis
			elif(geo_engine.lower() == 'yahoo'):
				g = geocoder.yahoo(complete_location)			
			#bing
			elif(geo_engine.lower() == 'bing'):
				g = geocoder.bing(complete_location, key = 'NbUiTxM3ZsZof0mfRrts~iwCj0mVkMdct_nmYdghchg~AkdUKbDkypy_4zuKgSyuGcSxXw13Z2CNtjMMsYfjJOPZGZ1sEu1KpAp9xoW3h30a')
			#Error
			else:
				raise Exception('No support for engine: ' + geo_engine)						

			#If nothing is located, the default location is returned	
			if(len(g) == 0):
				 	return self.defult_location

			return(np.array(g.latlng))

		except Exception as e:
			print(e)
			return self.defult_location




locator = Geolocator(['google','arcgis','bing'])
coordinates = locator.get_coordinates(address = 'CLL 131A 9')
print(coordinates)
print(locator.get_error(coordinates))


