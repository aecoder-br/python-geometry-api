import os
from fastapi import FastAPI, HTTPException
import alphashape
import numpy as np
from shapely.geometry import mapping
from models.points import Points
from dotenv import load_dotenv


load_dotenv()

app = FastAPI()

@app.post("/2d_concave_hull/")
def get_2d_concave_hull(points: Points, alpha: float = 0.0):
	try:
		# Convert the list of points to a numpy array
		np_points = np.array(points.points)
		# Generate the alpha shape
		concave_hull = alphashape.alphashape(np_points, alpha)
		# Extract the edges of the alpha shape
		#edges = list(mapping(concave_hull)['coordinates'])
		if concave_hull.geom_type == "GeometryCollection":
			# Get the first geometry
			concave_hull = concave_hull[0]

		edges = []
		if concave_hull.geom_type == "Polygon":
			edges = list(concave_hull.exterior.coords)
		elif concave_hull.geom_type == "MultiPolygon":
			for polygon in concave_hull:
				edges.append(list(polygon.exterior.coords))
		elif concave_hull.geom_type == "LineString":
			edges = list(concave_hull.coords)
		elif concave_hull.geom_type == "MultiLineString":
			for line in concave_hull:
				edges.append(list(line.coords))
		return {"edges": edges}
	except Exception as e:
		# Get the error message
		msg = str(e)
		print(msg)
		
		raise HTTPException(status_code=500, detail=msg)

if __name__ == "__main__":
	import uvicorn
	uvicorn.run(app, host="0.0.0.0", port=8000)
