#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Script for geolocating adresses
#This script uses intensivly geocoder

import numpy as np
import geocoder
import os
import pandas as pd
from haversine import haversine, Unit


class Geolocator:

	#Initializer	
	def __init__(self, 
				engines = ['geocodefarm', 'arcgis','bing','osm', 'geolytica', 'ottawa'],
				output_file = "out.csv"):
		'''
		Parameters
		---------
		engines : array[string]
			Array of the engines that geocoder will use. Can be any of the following:
			- geocodefarm
			- arcgis
			- bing (api-key)
			- osm
			- geolytica
			- ottawa
		'''

		#Saves engines	
		self.engines = np.array(engines)

		self.output_file = output_file


	def get_error(self, coordinates_dic):
		'''		
		Gets the error of a given set of coordinates. The error corresponds to the diagonal of
		the smallest enclosing square
		
		Parameters
		---------
		coordinates_dic : dictionary
			A dictionary with latitude and longitude values for each engine
		
		Returns
		-------		

		error : float
			An average error of the locations (assuming they all refer to the same location)
		'''

		#Calculates the square
		c = np.array(list(coordinates_dic.values()))
		x = np.nanmin(c, axis = 0)
		y = np.nanmax(c, axis = 0)
		
		return np.round(haversine((x[0], x[1]), (y[0], y[1]), unit = "m"),2)



	def get_coordinates(self, address):
		'''
		Parameters
		----------
		address : string
			The asdress to search 
		
		Returns
		-------
		dict
			dictionary with the lat lon values for each engine
		'''

		eng = np.reshape(self.engines, (len(self.engines),1))

		latlng = np.apply_along_axis(lambda x: self.process_request(address,x[0]),1, eng)

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
			- geocodefarm
			- arcgis
			- bing (api-key)
			- osm
			- geolytica
			- ottawa
		-----------------------------
		Return
		coordinates : numpy array
			Two dimensional array with the lattitude and longitud (in that order)
		'''	
		try:
			#geocodefarm
			if(geo_engine.lower() == 'geocodefarm'):
				g = geocoder.geocodefarm(complete_location)		 
			#Argis
			elif(geo_engine.lower() == 'arcgis'):
				g = geocoder.arcgis(complete_location)
			#osm
			elif(geo_engine.lower() == 'osm'):
				g = geocoder.osm(complete_location)			
			#bing
			elif(geo_engine.lower() == 'bing'):
				g = geocoder.bing(complete_location, key = 'NbUiTxM3ZsZof0mfRrts~iwCj0mVkMdct_nmYdghchg~AkdUKbDkypy_4zuKgSyuGcSxXw13Z2CNtjMMsYfjJOPZGZ1sEu1KpAp9xoW3h30a')
			# geolytica
			elif(geo_engine.lower() == 'geolytica'):
				g = geocoder.geolytica(complete_location)	
			# ottawa
			elif(geo_engine.lower() == 'ottawa'):
				g = geocoder.ottawa(complete_location)	
			#Error
			else:
				raise Exception('No support for engine: ' + geo_engine)						
			
			# Checks
			if g.ok:
				return g.latlng
			
			return [np.nan, np.nan]

		except Exception as e:
			print(e)
			return [np.nan, np.nan]


	def export_response_to_file(self, address, resp, include_error = True):
		'''
		Method that writes a response to file.
		'''

		# Check if the file exists
		if not os.path.exists(self.output_file):
			# Create the file if it doesn't exist
			with open(self.output_file, 'w') as file:
				file.write(self.create_output_file_header(include_error = include_error) + '\n')

		with open(self.output_file, 'a') as file:
				file.write(self.create_output_file_line(address=address, resp=resp, include_error = include_error) + '\n')
		

	# Support Methods
	# ----------------------
	def create_output_file_header(self, include_error = True):
		
		header = "address,"
		header += ",".join([ f"{k}_lat,{k}_lon" for k in self.engines])

		if include_error:
			header += ",max_error" 

		return header

	def create_output_file_line(self, address, resp, include_error = True):
		
		response = f"{address},"

		lines = []
		for k in self.engines:

			val = ","
			if not pd.isna(resp[k][0]) and not pd.isna(resp[k][1]):
				val = f"{resp[k][0]},{resp[k][1]}"

			lines.append(val)

		response += ",".join(lines)

		if include_error:
			response += f",{self.get_error(resp)}" 

		return response




if __name__ == "__main__": 

	locator = Geolocator(['google','arcgis','bing'])
	coordinates = locator.get_coordinates(address = 'CLL 131A 9')
	print(coordinates)
	print(locator.get_error(coordinates))


