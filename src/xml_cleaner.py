from __future__ import annotations

import xml.etree.ElementTree as ET
from typing import Any, Dict


class XmlCleaner:
    @staticmethod
    def clean_xml(xml_string: str) -> Dict[str, Any]:
        root = ET.fromstring(xml_string)
        return {root.tag.upper(): [XmlCleaner._clean_element(root)]}

    @staticmethod
    def _clean_element(element: ET.Element) -> Dict[str, Any]:
        result: Dict[str, Any] = {key.upper(): value for key, value in element.attrib.items()}
        for child in element:
            tag = child.tag.upper()
            result.setdefault(tag, [])
            result[tag].append(XmlCleaner._clean_element(child))
        return result
