from cohortextractor import StudyDefinition, patients, codelist, codelist_from_csv


study = StudyDefinition(
    default_expectations={
        "date": {"earliest": "2020-02-01", "latest": "today"},
        "rate": "uniform",
        "incidence": 0.5,
    },
    index_date="2020-02-01",
    population=patients.satisfying(
        "registered AND first_positive_date",
        registered=patients.registered_as_of("index_date"),
    ),
    first_positive_date=patients.with_test_result_in_sgss(
        pathogen="SARS-CoV-2",
        test_result="positive",
        find_first_match_in_period=True,
        restrict_to_earliest_specimen_date=False,
        returning="date",
        date_format="YYYY-MM-DD",
    ),
    subsequent_positive=patients.with_test_result_in_sgss(
        pathogen="SARS-CoV-2",
        test_result="positive",
        on_or_after="first_positive_date + 1 days",
        restrict_to_earliest_specimen_date=False,
        return_expectations={"incidence": 0.5},
    ),
    last_positive_date=patients.with_test_result_in_sgss(
        pathogen="SARS-CoV-2",
        test_result="positive",
        on_or_after="first_positive_date + 1 days",
        find_last_match_in_period=True,
        restrict_to_earliest_specimen_date=False,
        returning="date",
        date_format="YYYY-MM-DD",
    ),
)
