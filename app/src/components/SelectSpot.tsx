import { useRoute } from '@react-navigation/native';
import React, { useState } from 'react';
import { View, Text, Button } from 'react-native';
import { ButtonGroup } from '@rneui/themed';
import { styles } from '../styles/styles';

interface DestinationProps {
  id: string;
  latitude: number;
  longitude: number;
}

interface SelectSpotProps {
  destination: DestinationProps;
}

enum Price {
  FREE = 'Free',
  ONE_DOLLAR = '$',
  TWO_DOLLARS = '$$',
  THREE_DOLLARS = '$$$'
}

enum Environment {
  ANY = 'Any',
  INDOOR = 'Indoor',
  OUTDOOR = 'Outdoor'
}

export function SelectSpot(){
  const route = useRoute()
  const { item } = route.params
  const [selectedIndexEnv, setSelectedIndexEnv] = useState(0);
  const [selectedIndexPrice, setSelectedIndexPrice] = useState(0);
  const buttonsEnv = [Environment.ANY, Environment.INDOOR, Environment.OUTDOOR];
  const buttonsPrice = [Price.FREE, Price.ONE_DOLLAR, Price.TWO_DOLLARS, Price.THREE_DOLLARS];
  
  const handleContinue = () => {
    // Implemente a lógica de prosseguir aqui
  }

  return (
    <View style={styles.selectSpotWrapper}>
      <View>
        <View style={styles.selectSpotTitle}>
          <Text style={{fontSize: 20}}>Parking: {item.id.toUpperCase()}</Text>
          <Text>ISEP Parking </Text>
        </View>

        <Text style={{fontSize: 20}}>Price</Text>
        <ButtonGroup
        selectedIndex={selectedIndexPrice}
        buttons={buttonsPrice}
        onPress={(value) => {
          setSelectedIndexPrice(value);
        }}
        containerStyle={{ marginBottom: 80 }} />

        <Text style={{fontSize: 20}}>Environment</Text>
        <ButtonGroup
        selectedIndex={selectedIndexEnv}
        buttons={buttonsEnv}
        onPress={(value) => {
          setSelectedIndexEnv(value);
        }} />
      </View>
      <Button title="Find Spot" onPress={handleContinue} />
    </View>
  );
};
