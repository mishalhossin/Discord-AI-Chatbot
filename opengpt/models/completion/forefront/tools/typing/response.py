from pydantic import BaseModel
from typing import List, Optional, Union

class EmailResponse(BaseModel):
	sessionID: str
	client: str

class DeltaResponse(BaseModel):
	content: Optional[Union[str, None]] = ''

class ChoicesResponse(BaseModel):
	index: int
	finish_reason: Optional[Union[str, None]] = ''
	delta: DeltaResponse
	usage: Optional[Union[str, None]] = ''

class ForeFrontResponse(BaseModel):
	model: str
	choices: List[ChoicesResponse]