from fastapi import APIRouter, HTTPException
from app.services.rag_service import rag_service
from app.models.schemas import QueryRequest, QueryResponse
from app.core.logger import logger
from app.services.agent_service import agent_service

router = APIRouter(prefix="/ask", tags=["RAG"])

@router.post("/", response_model=QueryResponse)
async def ask_question(request: QueryRequest):
    try:
        logger.info(f"Query received: {request.query}")
        
        # Call the RAG pipeline
        result = await agent_service.route_request(
            query=request.query, 
            history=[msg.model_dump() for msg in request.history] # Convert Pydantic to dict
        )
        
        return QueryResponse(
            answer=result["answer"],
            source=result["sources"], # Note: mapped to 'source' in your schema
            confidence=result["confidence"]
        )
    except Exception as e:
        logger.error(f"RAG Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal AI Error")
