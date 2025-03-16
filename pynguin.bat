@echo off
setlocal

docker run ^
    -it ^
    --rm ^
    -e PYTHONPATH=/input/codetiming_local:/input/docstring_parser_local:/input/flutes_local:/input/flutils_local:/input/mimesis_local:/input/pypara_local:/input/mimesis_local:/input/python-string-utils_local ^
    -v "%cd%\examples:/input:ro" ^
    -v "%cd%\tests:/output" ^
    -v "%cd%\pynguin-report:/app/pynguin-report" ^
    pynguin-cli ^
    --project-path "/input" ^
    --output-path "/output" ^
    --verbose ^
    %*
