import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import FontAwesome from 'react-native-vector-icons/FontAwesome';

export function Arrived () {
  return (
    <View style={styles.container}>
      <FontAwesome name="check-circle" size={150} color="green" />
      <Text style={styles.message}>You've arrived!</Text>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#ffffff',
  },
  message: {
    fontSize: 24,
    fontWeight: 'bold',
    marginTop: 20,
  },
});