import os
from pathlib import Path
import pytest
from hmpps_person_match_score.spark import spark


def get_jars():
    # TODO Remove hack to change directory up from tests
    if os.getcwd().endswith('tests'):
        os.chdir("..")

    # TODO Remove duplicate declaration of jar files
    j = ['scala-udf-similarity-0.0.8.jar', 'graphframes-0.8.0-spark3.0-s_2.12.jar']
    jar_paths = [os.path.join(os.getcwd(), 'hmpps_person_match_score/jars', jar) for jar in j]
    jars = ",".join(jar_paths)
    return jars


@pytest.fixture(scope="function")
def spark_session():
    session = spark(get_jars())
    yield session
