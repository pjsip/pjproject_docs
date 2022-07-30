import re

def fix_doc(doc):
    """
    Convert link in svg from something like:

    https://www.google.com/url?q=https://docs.pjsip.org/en/latest/api/pjsip.html&amp;sa=D&amp;source=editors&amp;ust=1659062031097535&amp;usg=AOvVaw2CjhVRBxeOR9yQX-LyohQ_"

    to:

    ../api/pjsip.html
    """
    doc = re.sub(r'href=".*?google.*?/api/([a-zA-Z0-9_\-]+)\.html.*?"', 
                 r'href="../api/\1.html"', 
                 doc, flags=re.I|re.MULTILINE)
    doc = re.sub(r'''target=['"]_blank['"]''', '', doc, flags=re.I|re.MULTILINE)
    return doc

def fix_file(in_file, out_file=None):
    with open(in_file, "r") as f:
        doc = f.read()

    doc = fix_doc(doc)
    with open(out_file or in_file, "w") as f:
        f.write(doc)


if __name__=='__main__':
    doc = '''
    <svg><blah><a xlink:href="https://www.google.com/url?q=https://docs.pjsip.org/en/latest/api/pjsip.html&amp;sa=D&amp;source=editors&amp;ust=1659062031097535&amp;usg=AOvVaw2CjhVRBxeOR9yQX-LyohQ_" target="_blank" rel="noreferrer"></blah>
      <blah><a xlink:href="https://www.google.com/url?q=https://docs.pjsip.org/en/latest/api/pjsip.html&amp;sa=D&amp;source=editors&amp;ust=1659062031097535&amp;usg=AOvVaw2CjhVRBxeOR9yQX-LyohQ_" target="_blank" rel="noreferrer"></blah>
    </svg>
    '''
    fix_file('PJPROJECT 2.0 Architecture.svg', 'architecture.svg')
    #print(fix_doc(doc))
