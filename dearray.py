import tifffile as tf
import numpy as np

from pathlib import Path
from PIL import Image

from shapely.geometry import shape
from tqdm import tqdm

import json

class TMADearray():
	def __init__(self) -> None:
		pass

	def read_json(self, json_pth:Path) -> dict:
		with open(json_pth, "r") as f:
			json_dict = json.load(f)
		return json_dict

	def read_slide(self, slide_pth:Path) -> np.ndarray:
		with tf.TiffFile(slide_pth) as tfslide:           
			tfslide_arr = tfslide.asarray()

			return tfslide_arr

	def run(self, slide_pth:Path, tma_json_pth:Path, output_folder:Path) -> None:
		
		tma_json = self.read_json(tma_json_pth)
		feature_list = tma_json["features"]

		slide_arr = self.read_slide(slide_pth)

		count = 0

		for feature in tqdm(feature_list, desc="Writing Cores"):

			geometry = feature["geometry"]
			feature_polygon = shape(geometry)
			feature_polygon = feature_polygon.buffer(100)

			properties = feature["properties"]

			name = properties["name"]
			
			is_missing = properties["isMissing"]
			if is_missing:
				continue

			minx, miny, maxx, maxy = feature_polygon.bounds

			tma_arr = slide_arr[int(miny):int(maxy), int(minx):int(maxx), :]

			tma_img = Image.fromarray(tma_arr)

			tma_img.save(output_folder / f"{name}.png")

if __name__ == "__main__":

	slide_path = Path("C:/Users/chris/one-drive-beatson/OneDrive - University of Glasgow/projects/events/qupath-workshop-2024/sample-images/bl-tissue-microarray.svs")

	tma_json = Path("bl-tissue-microarray.geojson")

	output_folder = Path("cores")
	output_folder.mkdir(exist_ok=True)
	
	dearrayer = TMADearray()
	dearrayer.run(slide_path, tma_json, output_folder)
	