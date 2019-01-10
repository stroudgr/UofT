package directory_explorer;

import java.util.Map;
import java.util.Collection;
import java.util.HashMap;
import java.util.Iterator;

/**
 * The root of a tree representing a directory structure.
 */
public class FileNode {

	/** The name of the file or directory this node represents. */
	private String name;
	/** Whether this node represents a file or a directory. */
	private FileType type;
	/** This node's parent. */
	private FileNode parent;
	/**
	 * This node's children, mapped from the file names to the nodes. If type is
	 * FileType.FILE, this is null.
	 */
	private Map<String, FileNode> children;

	/**
	 * A node in this tree.
	 *
	 * @param name
	 *            the file
	 * @param parent
	 *            the parent node.
	 * @param type
	 *            file or directory
	 * @see buildFileTree
	 */
	public FileNode(String name, FileNode parent, FileType type) {
		this.name = name;
		this.parent = parent;
		this.type = type;
		children = new HashMap<String, FileNode>();
	}

	/**
	 * Find and return a child node named name in this directory tree, or null
	 * if there is no such child node.
	 *
	 * @param name
	 *            the file name to search for
	 * @return the node named name
	 */
	public FileNode findChild(String name) {
		// Returns any descendant node named name (not a direct child necessarily). Originally, I wrote 
		// this method so it would only return a direct child named name, but I changed it after reading: 
		// https://bb-2016-09.teach.cs.toronto.edu/t/a1-part2-findchild/414
		Iterator<FileNode> i = getChildren().iterator();
		
		// An arbitrary child of this node 
		FileNode child;
		// The result from recursively calling on child
		FileNode childsChild;
		
		while(i.hasNext()){
			child = i.next();
			
			if (child.name.equals(name))
				return child;

			// Looks in the subtree rooted at child
			childsChild = child.findChild(name);
			if (childsChild != null)
				return childsChild;
		}
		return null;
		
	}

	/**
	 * Return the name of the file or directory represented by this node.
	 *
	 * @return name of this Node
	 */
	public String getName() {
		return this.name;
	}

	/**
	 * Set the name of the current node
	 *
	 * @param name
	 *            of the file/directory
	 */
	public void setName(String name) {
		this.name = name;
	}

	/**
	 * Return the child nodes of this node.
	 *
	 * @return the child nodes directly underneath this node.
	 */
	public Collection<FileNode> getChildren() {
		return this.children.values();
	}

	/**
	 * Return this node's parent.
	 * 
	 * @return the parent
	 */
	public FileNode getParent() {
		return parent;
	}

	/**
	 * Set this node's parent to p.
	 * 
	 * @param p
	 *            the parent to set
	 */
	public void setParent(FileNode p) {
		this.parent = p;
	}

	/**
	 * Add childNode, representing a file or directory named name, as a child of
	 * this node.
	 * 
	 * Precondition: this node is a directory
	 * 
	 * @param name
	 *            the name of the file or directory
	 * @param childNode
	 *            the node to add as a child
	 */
	public void addChild(String name, FileNode childNode) {
		this.children.put(name, childNode);
	}

	/**
	 * Return whether this node represents a directory.
	 * 
	 * @return whether this node represents a directory.
	 */
	public boolean isDirectory() {
		return this.type == FileType.DIRECTORY;
	}
	/**
	 * Return a string representation of a FileNode, printing its type followed 
	 * by its name.
	 * 
	 *  @return a string representation of a File Node
	 */
	public String toString(){
		
		if (this.isDirectory()){
			return "Directory: " + this.getName();
		}
		return "File: " + this.getName();
	}

	/**
	 * This method is for code that tests this class.
	 * 
	 * @param args
	 *            the command line args.
	 */
	public static void main(String[] args) {
		
	}

}
