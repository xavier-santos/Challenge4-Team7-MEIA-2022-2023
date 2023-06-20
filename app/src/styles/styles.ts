import { StyleSheet } from 'react-native';

export const styles = StyleSheet.create({
    container: {
      flex: 1,
      backgroundColor: '#fff',
      alignItems: 'center',
      justifyContent: 'center',
    },
    selectSpotWrapper: {
        flex: 1, 
        marginHorizontal: 10, 
        justifyContent: 'space-between'
    },
    selectSpotTitle: {
        marginVertical: 60,
        paddingBottom: 20, 
        borderBottomWidth: 1, 
        borderBottomColor: 'gray', 
        flex: 0, 
        gap: 10
    }
  });