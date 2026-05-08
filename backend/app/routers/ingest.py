from fastapi import APIRouter, HTTPException
from app.services.ingestion_service import ingestion_service
from app.models.schemas import IngestionResponse
from app.core.logger import logger

router = APIRouter(prefix="/ingest", tags=["Ingestion"])

@router.post("/", response_model=IngestionResponse)
async def trigger_ingestion():
    try:
        logger.info("Manual ingestion triggered via API.")
        count = ingestion_service.ingest_all_documents()
        
        return IngestionResponse(
            status="success",
            documents_processed=count,
            message=f"Successfully ingested {count} chunks into Pinecone."
        )
    except Exception as e:
        logger.error(f"Ingestion failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Document ingestion failed.")
