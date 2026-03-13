import pathlib
def fix(f):
    p = pathlib.Path(f)
    text = p.read_bytes().decode('utf-8-sig', errors='ignore')
    try:
        orig = text.encode('windows-1252').decode('utf-8')
        # Also do the 025 to 045 replacement properly just in case
        orig = orig.replace('DEP-ENG-025', 'DEP-ENG-045')
        p.write_bytes(orig.encode('utf-8'))
        print(f"Fixed {f}")
    except Exception as e:
        print(f"Failed {f}: {e}")

fix('CCP_Technical_Architecture.md')
fix('FR1_Genesis_Pipeline_Tech_Spec.md')
