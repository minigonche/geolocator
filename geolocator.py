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
			- bing (api-key) #NbUiTxM3ZsZof0mfRrts~iwCj0mVkMdct_nmYdghchg~AkdUKbDkypy_4zuKgSyuGcSxXw13Z2CNtjMMsYfjJOPZGZ1sEu1KpAp9xoW3h30a
		-----------------------------
		'''
	    
	    #Saves engines	
	    self.engines = engines

	    #Default location (North Pole Bitches!)
	    self.defult_location = np.array([90,180])


    
	def get_error(self, coordinates):
		'''
		Description
		Gets the error of a given set of coordinates. The error corresponds to the distance it will take
		to visit each coordinate sequentially untill returning to the origin.
		-----------------------------
		Parameters
		-----------------------------
		coordinates : numpy array
			A numpy array of shape (N,2) with N lat, long coordinates of a same address 
		-----------------------------
		Return
		error : float
			An average error of the locations (assuming they all refer to the same location)
		'''
		#Earth radius in meters
		r = 6371000

		#Apply the haversine formula for the distance traveled by sequentially following the terms
		#https://en.wikipedia.org/wiki/Great-circle_distance

		#Shift the lat lng coordinates by one
		c = coordinates
		c_1 =  np.roll(coordinates,1,axis = 0)
		#Absolute angle distance		
		delta = np.abs(c - c_1)

		#Haversine formula for low float point precision systems
		sigma = np.sin((delta[:,0])/2)**2 + np.cos(c[:,0])*np.cos(c_1[:,0])*np.sin((delta[:,1])/2)**2
		sigma = 2*np.arcsin(sigma)

		return r*np.sum(sigma)



	def get_latlong(self, address, city = 'Bogota', country = 'Colombia'):
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


	def process_request(self, complete_location, engine):
	'''
	Description
	Gets the lattitude and longitud of a complete location, given an specific search engine
	-----------------------------
	Parameters
	-----------------------------
	complete_location : String
		locations complete adress (including city and country)
	engine : String
		String that geocoder will use. Can be any of the following:
		- arcgis (free)
		- google (request limit)
		- bing (api-key) 		
	-----------------------------
	Return
	coordinates : numpy array
		Two dimensional array with the lattitude and longitud (in that order)
	'''	

	#Google
	if(engine.lower() == 'google'):

		 g = geocoder.google(complete_location)
		 if(len(g) == 0):
		 	return self.defult_location
		 return np.array(g.latlng)

	#Argis
	if(engine.lower() == 'arcgis'):
		








