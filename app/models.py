from pydantic import BaseModel, Field
from typing import Union, List
from humps import camel

def to_camel(string):
    return camel.case(string)


class CamelModel(BaseModel):
    class Config:
        alias_generator = to_camel
        populate_by_name = True


class SignedUrls(BaseModel):
    presigned_urls: Union[list[str] | None] = None


class PullResponse(CamelModel):
    status: Union[str, None] = None


class FileRequest(CamelModel):
    user_id: Union[str, None] = None
    file_name: Union[str, None] = None
    feature: Union[str, None] = None
    signed_url: Union[str, None] = None


class FileResponse(CamelModel):
    weaviate_id: Union[str, None] = None
    user_id: Union[str, None] = None
    file_name: Union[str, None] = None
    feature: Union[str, None] = None
    status: Union[str, None] = None
    error_detail: Union[str, None] = None
    

class User(BaseModel):
    cooperativa: Union[str | None] = Field(..., alias='cooperativa')
    email: Union[str | None] = Field(..., alias='email')
    login: Union[str | None] = Field(..., alias='login')
    descricao: Union[str | None] =Field(..., alias='descricao')
    cpf_cnpj: Union[str | None] = Field(..., alias='cpfCnpj')
    instituicao_origem: Union[str | None] = Field(..., alias='instituicaoOrigem')


class UserControlServicePayload(BaseModel):
    file_key: Union[str | None] = None
    service: Union[str | None] = None


class UserControlServiceResponse(BaseModel):
    message: Union[str | None] = None


class DocumentContent(BaseModel):
    _id: Union[str | None] = None
    date_time: Union[str | None] = None
    expireAt: Union[str | None] = None
    embeddings: Union[list[list[float]] | None] = None
    file_content: Union[str | None] = None
    file_key: Union[str | None] = None
    service: Union[str | None] = None
    user_id: Union[str | None] = None


class CheckDocumentsPayload(BaseModel):
    file_key: Union[str | None] = None
    service: Union[str | None] = None


class CheckDocumentsResponse(BaseModel):
    count: Union[int | None] = None
    documents: Union[list[DocumentContent] | None] = None


class DescriptionModel(BaseModel):
    type: Union[str | None] = None
    description: Union[str | None] = None


class PropertiesModel(BaseModel):
    question: Union[DescriptionModel | None] = None
    service: Union[DescriptionModel | None] = None
    model: Union[DescriptionModel | None] = None


class SourceModel(BaseModel):
    name: Union[str | None] = None
    link: Union[str | None] = None
    page: Union[int | None] = 0
    summary: Union[str | None] = 0
    topic_suggestions: Union[str, None] = None


class ConversationPayload(BaseModel):
    type: Union[str | None] = None
    start_date: Union[str | None] = None
    end_date: Union[str | None] = None
    properties: Union[PropertiesModel | None] = None
    file_name: Union[str | None] = None


class ConversationResponse(BaseModel):
    data: Union[str | None] = None
    success: bool = True


class NormativosResponse(BaseModel):
    message: Union[str | None] = None
    documents: Union[List | None] = None