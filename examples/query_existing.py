"""Read-only query of a pre-existing GPT Image task owned by your Key."""

import argparse

from gpt_image_crewai import GPTImageRetrieveTaskTool

p = argparse.ArgumentParser(description=__doc__)
p.add_argument("task_id")
a = p.parse_args()
print(GPTImageRetrieveTaskTool().run(task_id=a.task_id, wait_seconds=0))
