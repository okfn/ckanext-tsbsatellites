from ckanext.spatial.model.harvested_metadata import MappedXmlDocument, ISOElement


class ISODimension(ISOElement):

    elements = [
        ISOElement(
            name="name",
            search_paths=[
                'gmd:sequenceIdentifier/gco:MemberName/gco:aName/gco:CharacterString/text()',
            ],
            multiplicity='0..1',
        ),
        ISOElement(
            name="type",
            search_paths=[
                'gmd:sequenceIdentifier/gco:MemberName/gco:attributeType/gco:TypeName/gco:aName/gco:CharacterString/text()',
            ],
            multiplicity='0..1',
        ),
        ISOElement(
            name="descriptor",
            search_paths=[
                'gmd:sequenceIdentifier/gmd:descriptor/text()',
            ],
            multiplicity='0..1',
        ),

    ]


class CustomISODocument(MappedXmlDocument):

    elements = [
        ISOElement(
            name='content-info-attribute-description',
            search_paths=[
                'gmd:contentInfo/gmd:MD_CoverageDescription/gmd:attributeDescription/gco:RecordType/text()',
                'gmd:contentInfo/gmd:MD_ImageDescription/gmd:attributeDescription/gco:RecordType/text()',
            ],
            multiplicity="0..1",
        ),
        ISOElement(
            name='content-info-type',
            search_paths=[
                'gmd:contentInfo/gmd:MD_CoverageDescription/gmd:contentType/gmd:MD_CoverageContentTypeCode/@codeListValue',
                'gmd:contentInfo/gmd:MD_CoverageDescription/gmd:contentType/gmd:MD_CoverageContentTypeCode/text()',
                'gmd:contentInfo/gmd:MD_ImageDescription/gmd:contentType/gmd:MD_CoverageContentTypeCode/@codeListValue',
                'gmd:contentInfo/gmd:MD_ImageDescription/gmd:contentType/gmd:MD_CoverageContentTypeCode/text()',

            ],
            multiplicity="0..1",
        ),
        ISODimension(
            name='dimension',
            search_paths=[
                'gmd:contentInfo/gmd:MD_CoverageDescription/gmd:dimension/gmd:MD_RangeDimension',
                'gmd:contentInfo/gmd:MD_ImageDescription/gmd:dimension/gmd:MD_RangeDimension',
            ],
            multiplicity="*",
        ),
        ISOElement(
            name="frequency-of-collection",
            search_paths=[
                "gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent/gmd:temporalElement/gmd:EX_TemporalExtent/gmd:extent/gml:TimePeriod/gml:timeInterval/text()",
                "gmd:identificationInfo/srv:SV_ServiceIdentification/srv:extent/gmd:EX_Extent/gmd:temporalElement/gmd:EX_TemporalExtent/gmd:extent/gml:TimePeriod/gml:timeInterval/text()",
            ],
            multiplicity="*",
        ),
        ISOElement(
            name="frequency-of-collection-units",
            search_paths=[
                "gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent/gmd:temporalElement/gmd:EX_TemporalExtent/gmd:extent/gml:TimePeriod/gml:timeInterval/@unit",
                "gmd:identificationInfo/srv:SV_ServiceIdentification/srv:extent/gmd:EX_Extent/gmd:temporalElement/gmd:EX_TemporalExtent/gmd:extent/gml:TimePeriod/gml:timeInterval/@unit",
            ],
            multiplicity="*",
        ),

    ]

