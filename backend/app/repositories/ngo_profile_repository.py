from sqlalchemy import select
from sqlalchemy.orm import Session
from datetime import datetime, UTC

from app.models.ngo_profiles import NGOProfile
from app.models.enums import AccountType
from app.models.enums import VerificationStatus
from uuid import UUID

class NGOProfileRepository:

    def __init__(self,db: Session):
        self.db = db

    def create(
        self,
        *,
        user_id: UUID,
        dharpan_id: str,
        cert_doc_url: str,
        reg_doc_url: str,
    )->NGOProfile:
        ngo_profile = NGOProfile(
            user_id = user_id,
            dharpan_id = dharpan_id,
            cert_doct_url = cert_doc_url,
            reg_doc_url = reg_doc_url,
        )

        self.db.add(ngo_profile)
        self.db.commit()
        self.db.refresh(ngo_profile)

        return NGOProfile

    def get_by_id(self,ngo_id: UUID)-> NGOProfile|None:
        stmt = select(NGOProfile).where(NGOProfile.id == ngo_id)

        return self.db.scalar(stmt)
    
    def get_by_user_id(self,user_id: UUID) -> NGOProfile|None:
        stmt = select(NGOProfile).where(NGOProfile.user_id == user_id)

        return self.db.scalar(stmt)

    def save(self, ngo_profile: NGOProfile) -> NGOProfile:
        self.db.commit()
        self.db.refresh(ngo_profile)
        return ngo_profile

    def approve(self, ngo_profile: NGOProfile) -> NGOProfile:
        ngo_profile.verification_status = VerificationStatus.APPROVED
        ngo_profile.verified_at = datetime.now(UTC)
        ngo_profile.rejection_reason = None

        self.db.commit()
        self.db.refresh(ngo_profile)

        return ngo_profile
    
    def reject(self, ngo_profile: NGOProfile,reason: str) -> NGOProfile:
        ngo_profile.verification_status = VerificationStatus.REJECTED
        ngo_profile.rejection_reason = reason
        ngo_profile.verified_at = None

        self.db.commit()
        self.db.refresh(ngo_profile)

        return ngo_profile
    
    def list_pending(self) -> list[NGOProfile]:
        pending_ngos = self.db.query(NGOProfile).filter(NGOProfile.verification_status ==
            VerificationStatus.PENDING).all()
        return pending_ngos
    
    def list_verified(self) -> list[NGOProfile]:
        verified_ngos = self.db.query(NGOProfile).filter(NGOProfile.verification_status ==
            VerificationStatus.VERIFIED).all()
        return verified_ngos
    
    def list_rejected(self) -> list[NGOProfile]:

        return (
            self.db.query(NGOProfile)
            .filter(
                NGOProfile.verification_status ==
                VerificationStatus.REJECTED
            )
            .all()
        )
    def get_by_dharpan_id(
    self,
    dharpan_id: str,
    ) -> NGOProfile | None:

        return (
            self.db.query(NGOProfile)
            .filter(
                NGOProfile.dharpan_id == dharpan_id
            )
            .first()
        )


