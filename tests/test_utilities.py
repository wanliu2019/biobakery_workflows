
import unittest

from biobakery_workflows import utilities

class TestUtiltiesFunctions(unittest.TestCase):
    """ Test the functions found in the biobakery workflows utilities module """
    
    def test_taxa_remove_unclassified(self):
        """ Test the taxa remove unclassified function """
        
        taxa=["k__k1;p__p1;c__","k__k1;p__p1;c__c1;o__o1;f__f1;g__g1;s__s1",
              "k__k1;p__p1;c__c1;o__o1;f__f1;g__g1;s__"]
        expected_taxa=["k__k1;p__p1","k__k1;p__p1;c__c1;o__o1;f__f1;g__g1;s__s1",
              "k__k1;p__p1;c__c1;o__o1;f__f1;g__g1"]
        
        self.assertEqual(list(utilities.taxa_remove_unclassified(taxa)), expected_taxa)
        
    def test_taxa_remove_unclassified_spaces(self):
        """ Test the taxa remove unclassified function with spaces in names """
        
        taxa=["k__k1;p__p1 ; c__ ",
            "k__k1;p__p1;c__c1 ; o__o1 ;f__f1;g__g1 ; s__s1 ",
            "k__k1;p__p1;c__c1;o__o1;f__f1;g__g1;s__"]
        expected_taxa=["k__k1;p__p1",
            "k__k1;p__p1;c__c1;o__o1;f__f1;g__g1;s__s1",
            "k__k1;p__p1;c__c1;o__o1;f__f1;g__g1"]
        
        self.assertEqual(list(utilities.taxa_remove_unclassified(taxa)), expected_taxa)

    def test_taxa_by_level(self):
        """ Test the taxa by level function """
        
        taxa=["k__k1;p__p1;c__c1","k__k1;p__p1;c__c2","k__k1;p__p2;c__c3"]
        data=[[1,2],[1,2],[1,2]]
        expected_taxa=["k__k1;p__p1","k__k1;p__p2"]
        expected_data=[[2,4],[1,2]]
        
        actual_taxa, actual_data = utilities.taxa_by_level(taxa, data, 1)
        
        self.assertEqual(actual_taxa, expected_taxa)
        self.assertEqual(actual_data, expected_data)
        
    def test_taxa_by_level_kingdom(self):
        """ Test the taxa by level function set to merge to kingdom level"""
        
        taxa=["k__k1;p__p1;c__c1","k__k1;p__p1;c__c2","k__k1;p__p2;c__c3"]
        data=[[1,2],[1,2],[1,2]]
        expected_taxa=["k__k1"]
        expected_data=[[3,6]]
        
        actual_taxa, actual_data = utilities.taxa_by_level(taxa, data, 0)
        
        self.assertEqual(actual_taxa, expected_taxa)
        self.assertEqual(actual_data, expected_data)
        
    def test_taxa_by_level_strain(self):
        """ Test the taxa by level function set to merge to strain level"""
        
        taxa=["k__k1;p__p1;c__c1;o__o1;f__f1;g__g1;s__s1;t__t1","k__k1;p__p1;c__c2"]
        data=[[1,2],[1,2]]
        expected_taxa=["k__k1;p__p1;c__c1;o__o1;f__f1;g__g1;s__s1;t__t1"]
        expected_data=[[1,2]]
        
        actual_taxa, actual_data = utilities.taxa_by_level(taxa, data, 7)
        
        self.assertEqual(actual_taxa, expected_taxa)
        self.assertEqual(actual_data, expected_data)
        
    def test_taxa_by_level_strain_missing(self):
        """ Test the taxa by level function set to merge to strain level
            though there is no strain level input data """
        
        taxa=["k__k1;p__p1;c__c1;o__o1;f__f1;g__g1;s__s1","k__k1;p__p1;c__c2"]
        data=[[1,2],[1,2]]
        expected_taxa=[]
        expected_data=[]
        
        actual_taxa, actual_data = utilities.taxa_by_level(taxa, data, 7)
        
        self.assertEqual(actual_taxa, expected_taxa)
        self.assertEqual(actual_data, expected_data)

    def test_taxa_by_level_unknown(self):
        """ Test the taxa by level function with one taxon that does not include that level"""
        
        taxa=["k__k1;p__p1","k__k1;p__p1;c__c2","k__k1;p__p2;c__c3"]
        data=[[1,2],[1,2],[1,2]]
        expected_taxa=["k__k1;p__p1;c__c2","k__k1;p__p2;c__c3"]
        expected_data=[[1,2],[1,2]]
        
        actual_taxa, actual_data = utilities.taxa_by_level(taxa, data, 2)
        
        self.assertEqual(sorted(actual_taxa), sorted(expected_taxa))
        self.assertEqual(actual_data, expected_data)
        
    def test_relative_abundance(self):
        """ Test the relative abundance function """
        
        data=[[1,2,3],[1,2,3],[1,1,1]]
        expected_relab=[[1/3.0,2/5.0,3/7.0],[1/3.0,2/5.0,3/7.0],[1/3.0,1/5.0,1/7.0]]
        
        self.assertEqual(utilities.relative_abundance(data),expected_relab)
        
    def test_taxa_shorten_name(self):
        """ Test the taxa shorten name function """
        
        taxa=["k__k1;p__p1;c__c1","k__k1;p__p1;c__c1;o__o1","k__k1;p__p1"]
        expected_taxa=["p__p1","p__p1","p__p1"]
        
        self.assertEqual(utilities.taxa_shorten_name(taxa, 1), expected_taxa)
        
    def test_taxa_shorten_name_remove_identifier(self):
        """ Test the taxa shorten name function with removing the identifier"""
        
        taxa=["k__k1;p__p1;c__c1","k__k1;p__p1;c__c1;o__o1","k__k1;p__p1"]
        expected_taxa=["p1","p1","p1"]
        
        self.assertEqual(utilities.taxa_shorten_name(taxa, 1, remove_identifier=True), expected_taxa)
        
    def test_terminal_taxa(self):
        """ Test the terminal taxa function """
        
        taxa=["k__k1;p__p1","k__k1;p__p1;c__c1","k__k2;p__p2","k__k3;p__p3;c__c2;o__o3"]
        data=[[1],[2],[3],[4]]
        
        # it is expected that order of the taxa will stay the same as the original input
        expected_taxa=["k__k1;p__p1;c__c1","k__k2;p__p2","k__k3;p__p3;c__c2;o__o3"]
        expected_data=[[2],[3],[4]]
        
        actual_taxa, actual_data = utilities.terminal_taxa(taxa, data)
        
        self.assertEqual(actual_taxa,expected_taxa)
        self.assertEqual(actual_data,expected_data)
        
    def test_terminal_taxa_duplicate(self):
        """ Test the terminal taxa function with two duplicate terminal taxa"""
        
        taxa=["k__k1;p__p1","k__k1;p__p1;c__c1","k__k2;p__p2","k__k3;p__p3;c__c2;o__o3","k__k3;p__p3;c__c2;o__o3"]
        data=[[1],[2],[3],[4],[5]]
        
        # it is expected that order of the taxa will stay the same as the original input
        expected_taxa=["k__k1;p__p1;c__c1","k__k2;p__p2","k__k3;p__p3;c__c2;o__o3"]
        expected_data=[[2],[3],[9]]
        
        actual_taxa, actual_data = utilities.terminal_taxa(taxa, data)
        
        self.assertEqual(actual_taxa,expected_taxa)
        self.assertEqual(actual_data,expected_data)
        
    def test_filter_zero_rows(self):
        """ Test the filter zero rows function """
        
        taxa=["k__k1;p__p1","k__k1;p__p1;c__c1","k__k2;p__p2","k__k3;p__p3;c__c2;o__o3","k__k3;p__p3;c__c2;o__o3"]
        data=[[1],[0],[3],[0],[5]]
        
        # it is expected that order of the taxa will stay the same as the original input
        expected_taxa=["k__k1;p__p1","k__k2;p__p2","k__k3;p__p3;c__c2;o__o3"]
        expected_data=[[1],[3],[5]]
        
        actual_taxa, actual_data = utilities.filter_zero_rows(taxa, data)
        
        self.assertEqual(actual_taxa,expected_taxa)
        self.assertEqual(actual_data,expected_data)       
        
        
        
        