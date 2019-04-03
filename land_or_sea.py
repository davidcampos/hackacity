import land_type

land_type.load_map()

lat = 41.207886
lon = -8.577679999999996
print("Land: ", not land_type.is_ocean_local(lat, lon))

lat = 41.134386
lon = -8.67968
print("Ocean: ", land_type.is_ocean_local(lat, lon))