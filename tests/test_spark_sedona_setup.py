import pyspark
import sedona
from sedona.spark import SedonaContext

def test_pyspark_version():
    assert pyspark.__version__ == "3.5.9"

def test_sedona_import():
    assert sedona is not None

def test_sedona_context_import():
    assert SedonaContext is not None
