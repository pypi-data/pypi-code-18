import pytest

@pytest.fixture
def badge_outputs():
    return {
        "generator_svg": '' + \
            '<?xml version="1.0" encoding="UTF-8"?>\n' + \
            '<svg xmlns="http://www.w3.org/2000/svg" width="99" height="20">\n' + \
                '<linearGradient id="b" x2="0" y2="100%">\n' + \
                    '<stop offset="0" stop-color="#bbb" stop-opacity=".1"/>\n' + \
                    '<stop offset="1" stop-opacity=".1"/>\n' + \
                '</linearGradient>\n' + \
                '<mask id="a">\n' + \
                    '<rect width="99" height="20" rx="3" fill="#fff"/>\n' + \
                '</mask>\n' + \
                '<g mask="url(#a)">\n' + \
                    '<path fill="#555" d="M0 0h63v20H0z"/>\n' + \
                    '<path fill="#dfb317" d="M63 0h36v20H63z"/>\n' + \
                    '<path fill="url(#b)" d="M0 0h99v20H0z"/>\n' + \
                '</g>\n' + \
                '<g fill="#fff" text-anchor="middle" font-family="DejaVu Sans,Verdana,Geneva,sans-serif" font-size="11">\n' + \
                    '<text x="31.5" y="15" fill="#010101" fill-opacity=".3">coverage</text>\n' + \
                    '<text x="31.5" y="14">coverage</text>\n' + \
                    '<text x="80" y="15" fill="#010101" fill-opacity=".3">80%</text>\n' + \
                    '<text x="80" y="14">80%</text>\n' + \
                '</g>\n' + \
            '</svg>\n' + \
        '',
        "s3_svg": "",
    }