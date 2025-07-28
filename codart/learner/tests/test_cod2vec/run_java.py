import subprocess
import os


def run_java_extractor():
    process = subprocess.Popen(
        [
            "java",
            "-jar",
            os.path.join(
                "codart",
                "learner",
                "cod2vec",
                "JavaExtractor",
                "JPredict",
                "target",
                "JavaExtractor-0.0.1-SNAPSHOT.jar",
            ),
        ]
    )
    try:
        process.wait()
    except KeyboardInterrupt:
        process.terminate()
