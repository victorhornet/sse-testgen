@echo off
setlocal

docker run ^
    -it ^
    --rm ^
    -v "%cd%\examples:/input:ro" ^
    -v "%cd%\tests:/output" ^
    -v "%cd%\pynguin-report:/app/pynguin-report" ^
    pynguin-cli ^
    --project-path "/input" ^
    --output-path "/output" ^
    --verbose ^
    %*
