import logging
import datacompy
from PIL import Image
from .encry import md5
from dictdiffer import diff
from pandas import DataFrame
from WeTest.util import path
from pixelmatch.contrib.PIL import pixelmatch
from jsonschema import validate, draft7_format_checker
from jsonschema.exceptions import SchemaError, ValidationError


def campare_df(source: DataFrame, target: DataFrame, join_columns: list) -> bool:

    result = datacompy.Compare(
        df1=source,
        df2=target,
        join_columns=join_columns,
        df1_name="source",
        df2_name="target",
    )

    if result.matches():
        return True

    else:
        logging.error("{}\n{}".format(("=" * 100), result.report()))

        return False


def campare_dict(source: dict, target: dict) -> bool:

    result = diff(source, target)
    return list(result)


def campare_list(source: list, target: list) -> bool:

    return sorted(source) == sorted(target)


def campare_file(source: str, target: str) -> bool:

    return md5(source, "file") == md5(target, "file")


def campre_image(source: str, target: str, threshold: float = 0.1, includeAA=True, **kwargs) -> bool:

    ori = source
    source = Image.open(source)
    target = Image.open(target)
    diff = Image.new("RGBA", source.size)

    pixels = pixelmatch(source, target, diff, threshold=threshold, includeAA=includeAA, **kwargs)

    is_match = True
    if pixels > 0:
        is_match = False
        output = path.replace_name(ori, "source_target_diff")
        logging.info(f"Not match, see {output} for details")
        diff.save(output)

    return is_match


def campare_schema(json: dict, schema: dict) -> bool:

    try:
        validate(instance=json, schema=schema, format_checker=draft7_format_checker)
        return True

    except SchemaError as e:
        logging.error(f"SchemaError: {e.message}")
        return False

    except ValidationError as e:
        logging.error(f"ValidationError: {e.message}")
        return False
