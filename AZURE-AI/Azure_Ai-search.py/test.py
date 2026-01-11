import azure.search.documents.indexes as models
print(dir(models))
'''
['SearchIndexClient', 'SearchIndexerClient', '__all__', '__builtins__', '__cached__', 
'__doc__', '__file__', '__loader__', '__name__', '__package__', '__path__', '__spec__',
 '_generated', '_search_index_client', '_search_indexer_client', '_utils', 'models']

'''
print()
print()
print()
print('*'*50)
print()
print()
print()

import azure.search.documents.indexes.models as models
print(dir(models))



'''

['AIFoundryModelCatalogName', 'AIServices', 'AIServicesAccountIdentity', 
'AIServicesAccountKey', 'AIServicesVisionParameters', 'AIServicesVisionVectorizer', 'AnalyzeResult', 
'AnalyzeTextOptions', 'AnalyzedTokenInfo', 'AsciiFoldingTokenFilter', 'AzureBlobKnowledgeSource',
'AzureBlobKnowledgeSourceParameters', 'AzureMachineLearningParameters', 'AzureMachineLearningSkill', 
'AzureMachineLearningVectorizer', 'AzureOpenAIEmbeddingSkill', 'AzureOpenAIModelName', 'AzureOpenAITokenizerParameters',
'AzureOpenAIVectorizer', 'AzureOpenAIVectorizerParameters', 'BM25SimilarityAlgorithm', 'BinaryQuantizationCompression',
'BlobIndexerDataToExtract', 'BlobIndexerImageAction', 'BlobIndexerPDFTextRotationAlgorithm', 'BlobIndexerParsingMode', 
'CharFilter', 'CharFilterName', 'ChatCompletionExtraParametersBehavior', 'ChatCompletionResponseFormat', 
'ChatCompletionResponseFormatJsonSchemaProperties', 'ChatCompletionResponseFormatType', 'ChatCompletionSchema',
'ChatCompletionSkill', 'CjkBigramTokenFilter', 'CjkBigramTokenFilterScripts', 'ClassicSimilarityAlgorithm', 
'ClassicTokenizer', 'CognitiveServicesAccount', 'CognitiveServicesAccountKey', 'CommonGramTokenFilter', 
'CommonModelParameters', 'CompletedSynchronizationState', 'ComplexField', 'ConditionalSkill', 'ContentUnderstandingSkill', 
'ContentUnderstandingSkillChunkingProperties', 'ContentUnderstandingSkillChunkingUnit', 'ContentUnderstandingSkillExtractionOptions', 
'CorsOptions', 'CustomAnalyzer', 'CustomEntity', 'CustomEntityAlias', 'CustomEntityLookupSkill', 
'CustomEntityLookupSkillLanguage', 'CustomNormalizer', 'DataChangeDetectionPolicy', 'DataDeletionDetectionPolicy', 
'DataSourceCredentials', 'DefaultCognitiveServicesAccount', 'DictionaryDecompounderTokenFilter', 'DistanceScoringFunction', 
'DistanceScoringParameters', 'DocumentExtractionSkill', 'DocumentIntelligenceLayoutSkill', 
'DocumentIntelligenceLayoutSkillChunkingProperties', 'DocumentIntelligenceLayoutSkillChunkingUnit', 
'DocumentIntelligenceLayoutSkillExtractionOptions', 'DocumentIntelligenceLayoutSkillMarkdownHeaderDepth', 
'DocumentIntelligenceLayoutSkillOutputFormat', 'DocumentIntelligenceLayoutSkillOutputMode', 'DocumentKeysOrIds', '
EdgeNGramTokenFilter', 'EdgeNGramTokenFilterSide', 'EdgeNGramTokenizer', 'ElisionTokenFilter', 'EntityCategory', 
'EntityLinkingSkill', 'EntityRecognitionSkill', 'EntityRecognitionSkillLanguage', 'EntityRecognitionSkillVersion', 
'ExhaustiveKnnAlgorithmConfiguration', 'ExhaustiveKnnParameters', 'FieldMapping', 'FieldMappingFunction', 
'FreshnessScoringFunction', 'FreshnessScoringParameters', 'GetIndexStatisticsResult', 'HighWaterMarkChangeDetectionPolicy', 
'HnswAlgorithmConfiguration', 'HnswParameters', 'ImageAnalysisSkill', 'ImageAnalysisSkillLanguage', 'ImageDetail', 
'IndexProjectionMode', 'IndexStatisticsSummary', 'IndexedOneLakeKnowledgeSource', 'IndexedOneLakeKnowledgeSourceParameters', 
'IndexedSharePointContainerName', 'IndexedSharePointKnowledgeSource', 'IndexedSharePointKnowledgeSourceParameters', 
'IndexerCurrentState', 'IndexerExecutionEnvironment', 'IndexerExecutionResult', 'IndexerExecutionStatus', 
'IndexerPermissionOption', 'IndexerResyncBody', 'IndexerResyncOption', 'IndexerRuntime', 'IndexerStatus', 
'IndexingMode', 'IndexingParameters', 'IndexingParametersConfiguration', 'IndexingSchedule', 'InputFieldMappingEntry', 
'KeepTokenFilter', 'KeyPhraseExtractionSkill', 'KeyPhraseExtractionSkillLanguage', 'KeywordMarkerTokenFilter', 
'KeywordTokenizer', 'KeywordTokenizerV2', 'KnowledgeBase', 'KnowledgeBaseAzureOpenAIModel', 'KnowledgeBaseModel', 
'KnowledgeBaseModelKind', 'KnowledgeRetrievalLowReasoningEffort', 'KnowledgeRetrievalMediumReasoningEffort', 
'KnowledgeRetrievalMinimalReasoningEffort', 'KnowledgeRetrievalOutputMode', 'KnowledgeRetrievalReasoningEffort', 
'KnowledgeRetrievalReasoningEffortKind', 'KnowledgeSource', 'KnowledgeSourceAzureOpenAIVectorizer', 
'KnowledgeSourceContentExtractionMode', 'KnowledgeSourceIngestionParameters', 'KnowledgeSourceIngestionPermissionOption', 
'KnowledgeSourceKind', 'KnowledgeSourceReference', 'KnowledgeSourceStatistics', 'KnowledgeSourceStatus', 
'KnowledgeSourceSynchronizationStatus', 'KnowledgeSourceVectorizer', 'LanguageDetectionSkill', 'LengthTokenFilter', 
'LexicalAnalyzer', 'LexicalAnalyzerName', 'LexicalNormalizer', 'LexicalNormalizerName', 'LexicalTokenizer', 
'LexicalTokenizerName', 'LimitTokenFilter', 'LuceneStandardAnalyzer', 'LuceneStandardTokenizer', 'MagnitudeScoringFunction', 
'MagnitudeScoringParameters', 'MappingCharFilter', 'MarkdownHeaderDepth', 'MarkdownParsingSubmode', 'MergeSkill', 
'MicrosoftLanguageStemmingTokenizer', 'MicrosoftLanguageTokenizer', 'MicrosoftStemmingTokenizerLanguage', 
'MicrosoftTokenizerLanguage', 'NGramTokenFilter', 'NGramTokenizer', 'NativeBlobSoftDeleteDeletionDetectionPolicy', 
'OcrLineEnding', 'OcrSkill', 'OcrSkillLanguage', 'OutputFieldMappingEntry', 'PIIDetectionSkill', 
'PIIDetectionSkillMaskingMode', 'PathHierarchyTokenizer', 'PathHierarchyTokenizerV2', 'PatternAnalyzer', 
'PatternCaptureTokenFilter', 'PatternReplaceCharFilter', 'PatternReplaceTokenFilter', 'PatternTokenizer', 
'PermissionFilter', 'PhoneticEncoder', 'PhoneticTokenFilter', 'RankingOrder', 'RegexFlags', 
'RemoteSharePointKnowledgeSource', 'RemoteSharePointKnowledgeSourceParameters', 'RescoringOptions', 
'ResourceCounter', 'ScalarQuantizationCompression', 'ScalarQuantizationParameters', 'ScoringFunction', 
'ScoringFunctionAggregation', 'ScoringFunctionInterpolation', 'ScoringProfile', 'SearchAlias', 'SearchField', 
'SearchFieldDataType', 'SearchIndex', 'SearchIndexFieldReference', 'SearchIndexKnowledgeSource', 
'SearchIndexKnowledgeSourceParameters', 'SearchIndexPermissionFilterOption',
'SearchIndexer', 'SearchIndexerCache', 'SearchIndexerDataContainer', 'SearchIndexerDataIdentity', 
'SearchIndexerDataNoneIdentity', 'SearchIndexerDataSourceConnection', 'SearchIndexerDataSourceType', 
'SearchIndexerDataUserAssignedIdentity', 'SearchIndexerError', 'SearchIndexerIndexProjection', 
'SearchIndexerIndexProjectionSelector', 'SearchIndexerIndexProjectionsParameters', 'SearchIndexerKnowledgeStore', 
'SearchIndexerKnowledgeStoreBlobProjectionSelector', 'SearchIndexerKnowledgeStoreFileProjectionSelector', 
'SearchIndexerKnowledgeStoreObjectProjectionSelector', 'SearchIndexerKnowledgeStoreProjection', 
'SearchIndexerKnowledgeStoreProjectionSelector', 'SearchIndexerKnowledgeStoreTableProjectionSelector', 
'SearchIndexerLimits', 'SearchIndexerSkill', 'SearchIndexerSkillset', 'SearchIndexerStatus', 
'SearchIndexerWarning', 'SearchResourceEncryptionKey', 'SearchServiceCounters', 'SearchServiceLimits', 
'SearchServiceStatistics', 'SearchSuggester', 'SearchableField', 'SemanticConfiguration', 'SemanticField', 
'SemanticPrioritizedFields', 'SemanticSearch', 'SentimentSkill', 'SentimentSkillLanguage', 'SentimentSkillVersion', 
'ServiceIndexersRuntime', 'ShaperSkill', 'ShingleTokenFilter', 'SimilarityAlgorithm', 'SimpleField', 'SkillNames',
'SnowballTokenFilter', 'SnowballTokenFilterLanguage', 'SoftDeleteColumnDeletionDetectionPolicy', 'SplitSkill', 
'SplitSkillEncoderModelName', 'SplitSkillLanguage', 'SplitSkillUnit', 'SqlIntegratedChangeTrackingPolicy', 
'StemmerOverrideTokenFilter', 'StemmerTokenFilter', 'StemmerTokenFilterLanguage', 'StopAnalyzer', 'StopwordsList', 
'StopwordsTokenFilter', 'SuggestOptions', 'SynchronizationState', 'SynonymMap', 'SynonymTokenFilter', 'TagScoringFunction',
'TagScoringParameters', 'TextSplitMode', 'TextTranslationSkill', 'TextTranslationSkillLanguage', 'TextWeights',
'TokenCharacterKind', 'TokenFilter', 'TokenFilterName', 'TruncateTokenFilter', 'UaxUrlEmailTokenizer', 
'UniqueTokenFilter', 'VectorEncodingFormat', 'VectorSearch', 'VectorSearchAlgorithmConfiguration', 
'VectorSearchAlgorithmKind','VectorSearchAlgorithmMetric', 'VectorSearchCompression', 'VectorSearchCompressionKind',
'VectorSearchCompressionRescoreStorageMethod', 'VectorSearchCompressionTarget', 'VectorSearchProfile',
'VectorSearchVectorizer', 'VectorSearchVectorizerKind', 'VisionVectorizeSkill', 'VisualFeature', 'WebApiSkill',
'WebApiVectorizer', 'WebApiVectorizerParameters', 'WebKnowledgeSource', 'WebKnowledgeSourceDomain', 
'WebKnowledgeSourceDomains', 'WebKnowledgeSourceParameters', 'WordDelimiterTokenFilter', '__all__',
'__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__path__',
 '__spec__', '_edm', '_index', '_models']




'''



print('^' * 50)

from azure.search.documents.indexes import SearchIndexClient

print(dir(SearchIndexClient))

'''
['_ODATA_ACCEPT', '__annotations__', '__class__', '__delattr__', '__dict__', '__dir__',
 '__doc__', '__enter__', '__eq__', '__exit__', '__format__', '__ge__', '__getattribute__', '__gt__', 
 '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', 
 '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', 
 '__weakref__', '_headers', '_merge_client_headers', 'analyze_text', 'close', 'create_alias', 'create_index', 
 'create_knowledge_base', 'create_knowledge_source', 'create_or_update_alias', 'create_or_update_index', 
 'create_or_update_knowledge_base', 'create_or_update_knowledge_source', 'create_or_update_synonym_map',
   'create_synonym_map', 'delete_alias', 'delete_index', 'delete_knowledge_base', 'delete_knowledge_source', 
   'delete_synonym_map', 'get_alias', 'get_index', 'get_index_statistics', 'get_knowledge_base', 
   'get_knowledge_source', 'get_knowledge_source_status', 'get_search_client', 'get_service_statistics', 
   'get_synonym_map', 'get_synonym_map_names', 'get_synonym_maps', 'list_alias_names', 'list_aliases', 
   'list_index_names', 'list_index_stats_summary', 'list_indexes', 'list_knowledge_bases', 'list_knowledge_sources', 
   'send_request']'''
