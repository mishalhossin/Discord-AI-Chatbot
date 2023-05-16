from pydantic import BaseModel
from typing import Text

class ModelResponse(BaseModel):
	id: Text
	url: Text
	style: Text
	width: int
	height: int
