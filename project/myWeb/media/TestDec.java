import SCSL.*;

public final class TestDec
{
	public static void main(String[] args) 
	{
		String srcFile,dstFile;

		srcFile="c:/softcamp/03_Sample/test_Enc.xlsx";
		dstFile="c:/softcamp/03_Sample/test_Dec.xlsx";
	
		SLDsFile sFile = new SLDsFile();

		sFile.SettingPathForProperty("c:/softcamp/02_Module/02_ServiceLinker/softcamp.properties"); 
		
		int retVal = sFile.CreateDecryptFileDAC (
		"c:/softcamp/04_KeyFile/keyDAC_SVR0.sc",
		"SECURITYDOMAIN",
		srcFile,
		dstFile);
		System.out.println("CreateDecryptFileDAC [" + retVal + "]");
	}
}
