import unittest

from blocknode import BlockType, block_to_block_type


class TestBlockToBlockType(unittest.TestCase):
    def test_heading(self):
        block = "### This is a headline"
        result = block_to_block_type(block)

        self.assertEqual(result, BlockType.HEADING)

    def test_no_heading(self):
        block = "#Not a heading.\nAlso not a heading."
        result = block_to_block_type(block)

        self.assertEqual(result, BlockType.PARAGRAPH)

    def test_code(self):
        block = "```def fun(x, y):\n\treturn x + y```"
        result = block_to_block_type(block)

        self.assertEqual(result, BlockType.CODE)


    def test_no_code(self):
            block = "```def fun(x, y):\n\treturn x + y``"
            result = block_to_block_type(block)

            self.assertEqual(result, BlockType.PARAGRAPH)


    def test_quote(self):
        block = ">Water is wet.\n\t\t\t- Smart Guy"
        result = block_to_block_type(block)

        self.assertEqual(result, BlockType.QUOTE)


    def test_no_quote(self):
        block = "<This is not a quote."
        result = block_to_block_type(block)

        self.assertEqual(result, BlockType.PARAGRAPH)



    def test_unordered_list(self):
        block = "- Item 1\n- Item 2"
        result = block_to_block_type(block)

        self.assertEqual(result, BlockType.UNOLIST)


    def test_no_unordered_list(self):
        block = "-Not a list\n- Not an item"
        result = block_to_block_type(block)

        self.assertEqual(result, BlockType.PARAGRAPH)



    def test_ordered_list(self):
        block = "1. I'm number one!\n2. Second!"
        result = block_to_block_type(block)

        self.assertEqual(result, BlockType.OLIST)


    def test_no_ordered_list1(self):
        block = "1.Not ordered list.\n1. Not ether."
        result = block_to_block_type(block)

        self.assertEqual(result, BlockType.PARAGRAPH)



    def test_no_ordered_list2(self):
        block = "2. Not ordered list.\n1. Not ether."
        result = block_to_block_type(block)

        self.assertEqual(result, BlockType.PARAGRAPH)
