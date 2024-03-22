@echo on

SET OMP_NUM_THREADS=24
ECHO %OMP_NUM_THREADS%

REM Iniciar run_mhm.bat esperando sua conclusão sem abrir uma nova janela.
cmd /c run_mhm.bat

REM Após a conclusão de run_mhm.bat, prosseguir com o script Python.
python ./ObjFUNC_KGE_SPAEF_EVP.py

exit