import json
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
def get_2d_concave_hull(points: Points, token: str, alpha: float = 0.0):
	
	if not os.getenv("VERIFICATION_TOKEN") in token:
		raise HTTPException(status_code=403, detail="Forbidden access")
	
	if not token or not points.points:
		raise HTTPException(status_code=400, detail="Invalid request")
	
	try:
		print(f"Received {len(points.points)} points")
		print(f"Alpha: {alpha}")
		
		# Convert the list of points to a numpy array
		np_points = np.array(points.points)
		# Generate the alpha shape
		concave_hull = alphashape.alphashape(np_points, alpha)
		# Extract the edges of the alpha shape
		edges = list(mapping(concave_hull)['coordinates'])

		return {"edges": edges}
	except Exception as e:
		# Get the error message
		msg = str(e)
		print(msg)
		
		raise HTTPException(status_code=500, detail=msg)

if __name__ == "__main__":
	import uvicorn
	uvicorn.run(app, host="0.0.0.0", port=8000)
