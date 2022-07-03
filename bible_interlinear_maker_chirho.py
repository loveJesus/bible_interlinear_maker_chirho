#!/usr/bin/env python3
# For God so loved the world, that He gave His only begotten Son, that all who believe in Him should not perish but have everlasting life
import argparse
import os
import re
import sys
from jinja2 import Environment, FileSystemLoader, select_autoescape

from collections import defaultdict


def init_parser_chirho() -> argparse.ArgumentParser:
    parser_chirho = argparse.ArgumentParser(
        usage="%(prog)s [options]",
        description='A tool to link a Bible Verse translations. Writes to STDOUT. '
                    'Currently requires diatheke to be installed from libsword, along '
                    'with the OSHB, TR and SpaRV1909 modules.',)
    parser_chirho.add_argument(
        '-v', '--version', action='version', version='%(prog)s 0.1')
    parser_chirho.add_argument(
        '-o', '--ot_key_chirho', type=str, required=False, help='Old Testament key')
    parser_chirho.add_argument(
        '-n', '--nt_key_chirho', type=str, required=False, help='New Testament key')
    return parser_chirho


def init_jinja2_chirho():
    env_chirho = Environment(
        loader=FileSystemLoader("jinja2_chirho"),
        autoescape=select_autoescape()
    )
    return env_chirho


class BibleInterlinearMakerChirho:
    VERSE_LINE_RE_CHIRHO = re.compile(r'^(((\w|\s)+)\s(\d+):(\d+):)\s+(.+)$')
    VERSION_LINE_RE_CHIRHO = re.compile(r'^\(\w+\)$')
    STRONGS_RE_CHIRHO = re.compile(r'<([GgHh](\d+)?)>')

    jinja2_env_chirho = init_jinja2_chirho()

    def __init__(self, key_chirho: str, ot_name_chirho: str, nt_name_chirho: str, is_old_testament_chirho: bool):
        self.key_chirho = key_chirho
        self.nt_name_chirho = nt_name_chirho
        self.ot_name_chirho = ot_name_chirho
        self.is_old_testament_chirho = is_old_testament_chirho
        self.zipped_dict_chirho = self._handle_translations_chirho()

    def _parse_strongs_to_common_chirho(self, strongs_str_chirho: str) -> str:
        """Hallelujah, parse the strongs key into a common format strongs key (uppercase no leading numbers, Hallelujah)."""
        return strongs_str_chirho[0].upper() + str(int(strongs_str_chirho[1:]))

    def _parse_bible_str_tokens_chirho(self, bible_str_chirho: str) -> list:
        """
        Hallelujah, parse the bible verse string into a list of
        dicts for each word or group of words with their related strongs key tokens that follow them.
        (words with Strongs concordance Hallelujah).
        """
        bible_tokens_chirho = []
        bible_str_list_chirho = bible_str_chirho.split()
        word_grouping_list_chirho = []
        for token_chirho in bible_str_list_chirho:
            # if token_chirho == "׃":
            #     continue  # Ignore the hebrew ending colon at this point
            if strongs_match_chirho := self.STRONGS_RE_CHIRHO.match(token_chirho):
                if not word_grouping_list_chirho:
                    if len(bible_tokens_chirho) == 0:
                        # If in here, we have a strongs number starting the verse
                        bible_tokens_chirho.append({
                            "strongs_chirho": [
                                self._parse_strongs_to_common_chirho(strongs_match_chirho.group(1))],
                            "words_chirho": []})
                    else:
                        # if we are here, there is more than one strongs number that identify the previous word grouping
                        bible_tokens_chirho[-1]["strongs_chirho"].append(
                            self._parse_strongs_to_common_chirho(strongs_match_chirho.group(1)))
                else:
                    bible_tokens_chirho.append({
                        "strongs_chirho": [
                            self._parse_strongs_to_common_chirho(strongs_match_chirho.group(1))],
                        "words_chirho": word_grouping_list_chirho})
                    word_grouping_list_chirho = []
            else:
                word_grouping_list_chirho.append(token_chirho)
        if word_grouping_list_chirho:
            # Hanging words with no strongs number
            bible_tokens_chirho.append({
                "strongs_chirho": [],
                "words_chirho": word_grouping_list_chirho})
        return bible_tokens_chirho

    def _parse_bible_str_dict_tokens_chirho(self, bible_str_dict_chirho: dict) -> dict:
        """Hallelujah, parse the bible string dict tokens (words with Strongs concordance Hallelujah)."""
        bible_dict_tokens_chirho = {
            key_chirho: self._parse_bible_str_tokens_chirho(str_chirho)
            for key_chirho, str_chirho in bible_str_dict_chirho.items()}
        return bible_dict_tokens_chirho

    def _parse_bible_str_chirho(self, bible_str_chirho: str) -> dict:
        """
        Hallelujah, prepare lines and strong numbers, ignore irrelevant lines and join together lines for each
        verse and store the string into a dict that is keyed by the verse number. Return that dict.
        """
        bible_dict_chirho = defaultdict(str)
        bible_str_chirho = bible_str_chirho.replace("<", " <").replace(">", "> ").split('\n')
        last_key_chirho = ""
        for line_chirho in bible_str_chirho:
            stripped_line_chirho = line_chirho.strip()
            if not stripped_line_chirho:  # Ignore blank lines
                continue
            # Ignore Bible Version lines
            if self.VERSION_LINE_RE_CHIRHO.match(stripped_line_chirho):
                continue
            match_chirho = self.VERSE_LINE_RE_CHIRHO.match(line_chirho)
            if match_chirho:
                last_key_chirho = match_chirho.group(1)
                content_chirho = match_chirho.group(6)
            else:
                content_chirho = stripped_line_chirho
            bible_dict_chirho[last_key_chirho] += content_chirho

        return bible_dict_chirho

    def _separate_chirho(self, original_chirho: list, new_chirho: list) -> list:
        """Hallelujah, separate original tokens, and place new tokens as close as possible to the original tokens"""
        new_copy_chirho = new_chirho.copy()
        separated_chirho = []
        old_translation_token_list_chirho = []

        for original_token_chirho in original_chirho:
            old_translation_token_list_chirho.append(" ".join(original_token_chirho["words_chirho"]))
            token_chirho = {
                "original_chirho": " ".join(old_translation_token_list_chirho),
                "new_chirho": []}
            current_strongs_set_chirho = set(original_token_chirho["strongs_chirho"])
            found_new_word_chirho = False
            found_idx_chirho = 0
            for new_idx_chirho, new_word_chirho in enumerate(new_copy_chirho):
                if len(set(new_word_chirho["strongs_chirho"]) & current_strongs_set_chirho) > 0:
                    found_new_word_chirho = True
                    found_idx_chirho = new_idx_chirho
                    break
            if found_new_word_chirho:
                words_chirho = new_copy_chirho.pop(found_idx_chirho)["words_chirho"]
                token_chirho["new_chirho"] = words_chirho
                separated_chirho.append(token_chirho)
                old_translation_token_list_chirho = []
        if old_translation_token_list_chirho:
            separated_chirho.append({
                "original_chirho": " ".join(old_translation_token_list_chirho),
                "new_chirho": []})
        return separated_chirho

    def _zip_bible_dict_tokens_chirho(
            self,
            bible_name_ol_chirho: str, bible_dict_ol_tokens_chirho: dict,
            bible_name_nl_chirho: str, bible_dict_nl_tokens_chirho: dict) -> dict:
        zipped_dict_chirho = {
            "original_name_chirho": bible_name_ol_chirho,
            "new_name_chirho": bible_name_nl_chirho,
            "verses_chirho": {}}
        ol_keys_chirho = set(bible_dict_ol_tokens_chirho.keys())
        nl_keys_chirho = set(bible_dict_nl_tokens_chirho.keys())
        if ol_keys_chirho != nl_keys_chirho:
            print("Keys do not match in NL and OL different verses in each translation - exiting")
            sys.exit(1)

        for ol_verse_key_chirho, ol_token_dict_chirho in bible_dict_ol_tokens_chirho.items():
            nl_token_dict_chirho = bible_dict_nl_tokens_chirho[ol_verse_key_chirho]
            zipped_dict_chirho["verses_chirho"][ol_verse_key_chirho] = {
                "original_chirho": ol_token_dict_chirho,
                "new_chirho": " ".join([
                    " ".join(nl_dict_chirho["words_chirho"]) for nl_dict_chirho in nl_token_dict_chirho]),
                "separated_chirho": self._separate_chirho(ol_token_dict_chirho, nl_token_dict_chirho)}

        return zipped_dict_chirho

    def _handle_translations_chirho(self):
        diatheke_ot_chirho = os.popen(
            f'diatheke -b {self.ot_name_chirho} -f plain -o vcan -k {self.key_chirho}').read()
        diatheke_nt_chirho = os.popen(
            f'diatheke -b {self.nt_name_chirho} -f plain -o vcan -k {self.key_chirho}').read()
        dict_ot_chirho = self._parse_bible_str_chirho(diatheke_ot_chirho)
        dict_nt_chirho = self._parse_bible_str_chirho(diatheke_nt_chirho)
        dict_ot_tokens_chirho = self._parse_bible_str_dict_tokens_chirho(dict_ot_chirho)
        dict_nt_tokens_chirho = self._parse_bible_str_dict_tokens_chirho(dict_nt_chirho)
        zipped_dict_chirho = self._zip_bible_dict_tokens_chirho(
            self.ot_name_chirho, dict_ot_tokens_chirho, self.nt_name_chirho, dict_nt_tokens_chirho)
        return zipped_dict_chirho

    def _verse_dict_chirho(self, verse_str_chirho: str, verse_dict_item_chirho: dict) -> dict:
        """Hallelujah, Convert a separated dict item to an HTML string"""
        separated_dict_items_chirho = verse_dict_item_chirho["separated_chirho"]
        verse_tables_chirho = []
        for separated_item_chirho in separated_dict_items_chirho:
            if len(separated_item_chirho["new_chirho"]) == 0 and len(separated_item_chirho["original_chirho"]) == 0:
                continue
            col3_letters_chirho = 12 if not self.is_old_testament_chirho else 25
            col_class_chirho = (
                "col-md-9"
                if (len(separated_item_chirho["original_chirho"]) / col3_letters_chirho) >= 2
                else "col-md-6"
                if (len(separated_item_chirho["original_chirho"]) / col3_letters_chirho) >= 1
                else "col-md-3")
            verse_tables_chirho.append({
                "col_class_chirho": col_class_chirho,
                "original_chirho": separated_item_chirho["original_chirho"],
                "new_chirho": " ".join(separated_item_chirho["new_chirho"])})

        reverse_class_chirho = "flex-row-reverse" if self.is_old_testament_chirho else ""

        return {
            "verse_str_chirho": verse_str_chirho,
            "new_chirho": verse_dict_item_chirho["new_chirho"],
            "verse_tables_chirho": verse_tables_chirho,
            "reverse_class_chirho": reverse_class_chirho}

    def get_translation_dict_chirho(self, zipped_dict_chirho: dict = None):
        """Hallelujah handle example:
            {
                "original_name_chirho": "WLC",
                "new_name_chirho": "SpaRV1909",
                "verses_chirho": {
                    "Genesis": {
                        "original_chirho": "In the beginning God created the heavens and the earth.",
                        "new_chirho": "In the beginning God created the heavens and the earth.",
                        "separated_chirho": [
                            {
                                "original_chirho": "beginning",
                                "new_chirho": ["In", "the", "beginning"]
                            },....
                        ]
                    }....
                }
            }
        """
        zipped_dict_chirho = zipped_dict_chirho or self.zipped_dict_chirho
        verses_chirho = []

        for bible_verse_str_chirho, bible_verse_value_chirho in zipped_dict_chirho["verses_chirho"].items():
            verses_chirho.append(
                self._verse_dict_chirho(bible_verse_str_chirho, bible_verse_value_chirho))

        return {
             "verses_chirho": verses_chirho,
             "original_name_chirho": zipped_dict_chirho["original_name_chirho"],
             "new_name_chirho": zipped_dict_chirho["new_name_chirho"]}


def main_chirho() -> None:
    parser_chirho = init_parser_chirho()
    args_chirho = parser_chirho.parse_args()
    ot_key_chirho = args_chirho.ot_key_chirho
    nt_key_chirho = args_chirho.nt_key_chirho
    print(
        f"Hallelujah parsing with OT: {ot_key_chirho} and NT: {nt_key_chirho}", file=sys.stderr)
    if not ot_key_chirho and not nt_key_chirho:
        print("God is good - No keys provided, run with -h to see help")
        sys.exit(1)

    translations_chirho = []

    if ot_key_chirho:
        ot_multi_ref_chirho = BibleInterlinearMakerChirho(ot_key_chirho, "OSHB", "SpaRV1909", True)
        translations_chirho.append(ot_multi_ref_chirho.get_translation_dict_chirho())

    if nt_key_chirho:
        nt_multi_ref_chirho = BibleInterlinearMakerChirho(nt_key_chirho, "TR", "SpaRV1909", False)
        translations_chirho.append(nt_multi_ref_chirho.get_translation_dict_chirho())

    jinja2_env_chirho = init_jinja2_chirho()
    html_content_chirho = jinja2_env_chirho.get_template("outermost_chirho.jinja2").render(
        enumerate=enumerate,
        translations_chirho=translations_chirho)

    print(html_content_chirho)


if __name__ == "__main__":
    main_chirho()
    sys.exit(0)
