
import time

from rich.progress import Progress

with Progress() as progress:

    task1 = progress.add_task("[red]Downloading...", total=10)
    while not progress.finished:
        progress.update(task1, advance=1)
        print('step1')
        time.sleep(1)
        progress.update(task1, advance=1)
        print('step2')
        time.sleep(1)
        progress.update(task1, advance=1)
        print('step3')
        time.sleep(1)
        progress.update(task1, advance=1)
        print('step4')
        time.sleep(1)
        progress.update(task1, advance=1)
        print('step5')
        time.sleep(1)
        progress.update(task1, advance=1)
        print('step6')
        time.sleep(1)
        progress.update(task1, advance=1)
        print('step7')
        time.sleep(1)
        progress.update(task1, advance=1)
        print('step8')
        time.sleep(1)
        progress.update(task1, advance=1)
        print('step9')
        time.sleep(1)
        progress.update(task1, advance=1)
        print('step10')
        time.sleep(1)
