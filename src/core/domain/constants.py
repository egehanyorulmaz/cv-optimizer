from pathlib import Path
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEST_FILE_PATH = PROJECT_ROOT / "tests" / "fixtures" / "sample_resume.pdf"

logger.info(f"PROJECT_ROOT: {PROJECT_ROOT}")
logger.info(f"TEST_FILE_PATH: {TEST_FILE_PATH}")
