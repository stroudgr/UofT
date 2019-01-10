package directory_reader;

import java.io.File;
import javax.swing.JFileChooser;

/**
 * Select, read, and print the contents of a directory.
 */
public class DirectoryReader {

	/**
	 * Select a directory, then print the full path to the directory and its
	 * contents, one per line. Prefix the contents with a hyphen and a space.
	 *
	 * @param args
	 *            the command line arguments
	 */
	public static void main(String[] args) {

		JFileChooser fileChooser = new JFileChooser();
		fileChooser.setFileSelectionMode(JFileChooser.DIRECTORIES_ONLY);
		int returnVal = fileChooser.showOpenDialog(null);

		if (returnVal == JFileChooser.APPROVE_OPTION) {
			File file = fileChooser.getSelectedFile();
			System.out.println(file);
			
			//All the files in the selected directory
			File contents[] = file.listFiles();
			
			for (int i=0; i < contents.length; i++){
				//Gets the name of the file 
				String sub = contents[i].toString();
				sub = sub.substring(file.toString().length() + 1);
				
				if (contents[i].isDirectory())
					System.out.println("- " + sub + "/");
				else
					System.out.println("- " + sub);
			}
			
		}
	}
}
