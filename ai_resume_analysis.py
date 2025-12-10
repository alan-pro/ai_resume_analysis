import sys
sys.path.insert(0, ".")
import uvicorn
import multiprocessing
from conf import cnf
from src.app import app

import platform
system = platform.system()

app_str = "ai_resume_analysis:app"

def __run():
    port = cnf.service.port
    # 如果是windows系统或者develop模式，使用uvicorn启动
    if cnf.runtime.mode == "develop" or system == 'Windows':
        uvicorn.run(app_str, host="0.0.0.0", port=port, log_level="debug", reload=True)
    else:
        from gunicorn.app.wsgiapp import run
        #进程数
        workers = multiprocessing.cpu_count() * 2 + 1
        sys.argv = ["gunicorn", app_str, "--workers", str(workers), "--timeout", "300", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", f"0.0.0.0:{port}", "--keep-alive", "300"]
        run()

if __name__ == "__main__":
    __run()