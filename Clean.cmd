@PUSHD %~dp0


:CLEAN
@FOR /D %%f in ("src\*.egg-info", build, dist) DO @(
  IF EXIST %%f (
    @RD /s /q %%f
  )
)
@GOTO DONE


:DONE
@POPD
