from uuid import UUID

from fastapi import HTTPException, status

from app.repositories.ngo_profile_repository import NGOProfileRepository
class NGOProfile:

    def __init__(self, repository: NGOProfileRepository):
        self.repository = repository

    def create_profile(
            self,
            *,
            user_id: UUID,
            dharpan_id: str,
            cert_doc_url: str,
            reg_doc_url: str):
        return self.repository.create(
            user_id = user_id,
            dharpan_id = dharpan_id,
            cert_doc_url = cert_doc_url,
            reg_doc_url = reg_doc_url
        ) 
    
    