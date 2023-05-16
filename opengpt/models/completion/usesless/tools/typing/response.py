from pydantic import BaseModel
from typing import List, Optional, Union

class DeltaResponse(BaseModel):
	content: Optional[Union[str, None]] = ''
	role: Optional[Union[str, None]] = ''

class ChoicesResponse(BaseModel):
	delta: DeltaResponse
	index: int
	finish_reason: Optional[Union[str, None]] = ''

class UseslessResponse(BaseModel):
	id: str
	object: str
	created: int
	model: str
	choices: List[ChoicesResponse]