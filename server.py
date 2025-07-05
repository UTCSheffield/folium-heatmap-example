from flask import Flask

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

import folium
from folium import plugins
from folium.plugins import HeatMap



app = Flask(__name__)


@app.route('/')
def index():
  df_acc = pd.read_csv('locations.csv', dtype=object)

  print(df_acc)

  m = folium.Map(location=[51.5074, 0.1278],
                      zoom_start = 11) # Uses lat then lon. The bigger the zoom number, the closer in you get

  # Ensure you're handing it floats
  df_acc['Latitude'] = df_acc['Latitude'].astype(float)
  df_acc['Longitude'] = df_acc['Longitude'].astype(float)

  df_acc = df_acc[['Latitude', 'Longitude']]
  df_acc = df_acc.dropna(axis=0, subset=['Latitude','Longitude'])

  # List comprehension to make out list of lists
  heat_data = [[row['Latitude'],row['Longitude']] for index, row in df_acc.iterrows()]
  # Plot it on the map
  HeatMap(heat_data).add_to(m)
  
  m.fit_bounds([[59.202939,-10.345844], [50.323020,2.31866]])
  fs = plugins.Fullscreen().add_to(m)
  
  m.fit_bounds(m.get_bounds(), padding=(30, 30))
  
  folium.TileLayer('stamentoner').add_to(m)
  folium.TileLayer('stamenwatercolor').add_to(m)
  folium.TileLayer('cartodbpositron').add_to(m)
  folium.TileLayer('openstreetmap').add_to(m)

  # Add the option to switch tiles
  folium.LayerControl().add_to(m)

  return m._repr_html_()

if __name__ == '__main__':
    app.run(debug=True)
