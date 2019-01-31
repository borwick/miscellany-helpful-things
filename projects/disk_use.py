#!/usr/bin/python
"""
This program helps you figure out where all your disk space has gone.

Two classes help: Folder, which stores disk use information for a
given folder, and Tree, which stores a bunch of folders and can
iterate along a path.  Tree also uses pickle to store information so
you don't have to hit your disk for each report you want to run.
"""
import os
import pickle

class Folder(object):
    """
    Folders store their path, a Folder parent (or None), and a size.
    When you add_size to them, the size gets added to all the folder's
    parents, too.  Thus, if /tmp/xyz/ is big, /tmp is big too.

    It's up to the caller to determine how 'size' is defined.

    A secret variable, self.my_size, stores just the size of the
    current folder.
    """
    def __init__( self, path, parent, size ):
        """
        Sets path, parent, initializes my_size and size to 0, and then
        calls self.add_size.
        """
        self.path = path
        self.parent = parent
        self.my_size = 0
        self.size = 0

        self.add_size( size )

    def _add_size( self, size ):
        """
        Increments self.size and calls self.parent._add_size(size).
        Notably, self.my_size is not incremented.
        """
        self.size += size
        if self.parent != None:
            self.parent._add_size( size )

    def add_size( self, size ):
        """
        Increments self.my_size and calls self._add_size.
        """
        self.my_size += size
        self._add_size( size )

    def get_size( self ):
        """
        Return self.size.
        """
        return self.size

    def get_parent( self ):
        """
        Return self.parent (as a Folder).
        """
        return self.parent

    def get_path( self ):
        """
        Return self.path.
        """
        return self.path

    def __str__( self ):
        """
        String representation is path followed by size (in bytes).
        """
        return '%s (%d)' % ( self.get_path(),
                             self.get_size() )

    def size_cmp( self, otro ):
        """
        Compare self with another object, by how big they are.
        """
        if isinstance( otro, Folder ):
            return cmp( self.size, otro.size )
        else:
            return 1

    def path_cmp( self, otro ):
        """
        Compare self with another object, by their path (or by their
        string representation if it's not a Folder).
        """
        if isinstance( otro, Folder ):
            return cmp( self.path, otro.path )
        else:
            return cmp( str( self ), str( otro ) )

    __cmp__ = path_cmp

class TreeException( Exception):
    """
    Any errors rooted in the tree class will be a subclass of
    TreeException.
    """
    pass

class Tree( object ):
    """
    Store a bunch of folders.  Two variables, self.folders and
    self.folder_index, keep track of folders.  self.folders is just an
    array; self.folder_index is a dictionary mapping paths to folders.
    """
    
    def __init__( self, tree_file ):
        """
        Init from a given file.  If the file does not exist, just init
        self.folders.  Call self._index_folders() to rebuild
        self.folder_index.
        """
        self.tree_file = tree_file

        # TODO: check to see if you can write to self.tree_file
        
        if os.path.exists( self.tree_file ):
            tree_fd = file( self.tree_file, 'r' )
            self.folders = pickle.load( tree_fd )
        else:
            self.folders = []

        self.folder_index = {}
        self._index_folders()

    def _index_folders( self ):
        """
        For each folder in self.get_folders, put it in
        self.folder_index.
        """
        for folder in self.folders:
            f_path = folder.get_path()
            self.folder_index[ f_path ] = folder

    def write( self ):
        """
        Use pickle to dump self.folders to a file.
        """
        tree_fd = file( self.tree_file, 'w' )
        pickle.dump( self.folders, tree_fd )

    def add_folder( self, folder ):
        """
        Add another folder to the Tree.  Exception raised if path
        already seen.
        """
        f_path = folder.get_path()
        
        if self.folder_index.has_key( f_path ):
            raise TreeException( "Already seen path '%s': can't add it!" \
                                 % f_path )
        else:
            self.folder_index[ f_path ] = folder
            self.folders.append( folder )

    def get_folder_by_path( self, path ):
        """
        Return exactly one folder given a path.
        """
        return self.folder_index[ path ]

    def get_folders_by_size( self, size ):
        """
        Return all folders greater than given size (in bytes).
        """
        ret_folders = []

        for folder in self.folders:
            if folder.get_size() >= size:
                ret_folders.append( folder )

        return ret_folders

    def walk_path( self, path ):
        """
        Use os.walk to iterate through the path.

        size is defined here to mean 'size of all regular files in
        bytes'.  Directory are (and softlink sizes) are ignored.
        """

        new_folder = Folder( path=path, parent=None, size=0 )
        self.add_folder( new_folder )
        
        for root, dirs, files in os.walk( path ):
            print root
            root_folder = self.get_folder_by_path( root )

            # create subdirectory folder objects
            for subdir in dirs:
                subdir_path = os.path.join( root, subdir )
                
                new_folder = Folder( path=subdir_path,
                                     parent=root_folder,
                                     size=0 )
                self.add_folder( new_folder )

            # add files to total folder size
            for subfile in files:
                subfile_path = os.path.join( root, subfile )
                if os.path.isfile( subfile_path ):
                    subfile_size = os.path.getsize( subfile_path )
                    root_folder.add_size( subfile_size )

    def __str__( self ):
        """
        Print out a junky representation of the tree.
        """
        retstr = ''
        retstr += "TREE:\n"
        for folder in self.folders:
            retstr += str( folder ) + '\n'
        return retstr

def pretty_size( size ):
    if size > 1024 ** 3:
        return '%.2fG' % ( size / 1024.0 ** 3 )
    elif size > 1024 ** 2:
        return '%.2fM' % ( size / 1024.0 ** 2 )
    elif size > 1024 ** 1:
        return '%.2fK' % ( size / 1024.0 )
    else:
        return '%dB' % size
    

if __name__ == '__main__':
    t = Tree( 'tree.dat' )
    t.walk_path( '/' )
    print 'initialized'
    for folder in t.get_folders_by_size( 1024 ** 2 * 100 ):
        print '%s (%s)' % ( folder.get_path(),
                            pretty_size( folder.get_size() )
                            )
    t.write()
