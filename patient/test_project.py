"""Small validation test for source data and transformations."""

from src.etl_pipeline import extract, transform


def test_etl_transformation():
    source = extract()
    cleaned, report = transform(source)

    assert len(source) == 12
    assert len(cleaned) > 0
    assert cleaned["visit_date"].notna().all()
    assert cleaned["treatment_expense"].notna().all()
    assert report["source_rows"] == 12


if __name__ == "__main__":
    test_etl_transformation()
    print("ETL validation test passed.")
