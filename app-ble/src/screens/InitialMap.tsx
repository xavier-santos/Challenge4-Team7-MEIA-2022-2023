import React, { useState, useRef, useMemo } from 'react';
import {View, Text, TextInput, FlatList, TouchableOpacity, Keyboard } from 'react-native';
import { BottomSheetModal, BottomSheetModalProvider } from '@gorhom/bottom-sheet';
import { GestureHandlerRootView } from 'react-native-gesture-handler';
import { LocationCoordProps } from '../types/types';
import { Map } from '../components/Map'
import { styles } from '../styles/styles';

export function InitialMap(props) {
  
  const parkings: LocationCoordProps[] = [{
    id: 'a',
    latitude: 41.17796324211171, 
    longitude: -8.60891994096156
  },
   {
    id: 'b',
    latitude: 41.17786497596217, 
    longitude: -8.608226428692205
   }, {
    id: 'c',
    latitude: 41.17832324568314, 
    longitude: -8.608156691263558
   }, {
    id: 'd',
    latitude: 41.1788158315874, 
    longitude: -8.608623395593737
   }]

   const ItemSeparatorView = () => {
    return (
      // Flat List Item Separator
      <View
        style={{
          height: 0.5,
          width: '100%',
          backgroundColor: '#C8C8C8',
        }}
      />
    );
  };
  const ItemView = ({item}: any ) => {
    return (
      // Flat List Item
      <TouchableOpacity  style={styles.itemStyle} onPress={() => handleSeletItem(item)}>
        <Text>{item.id.toUpperCase()} - ISEP Parking {item.id.toUpperCase()}</Text>
      </TouchableOpacity >
    );
  };

  const handleSeletItem = (item : LocationCoordProps) => {
    props.navigation.navigate('selectspot',{item})
  };

  const searchFilterFunction = (text: string) => {
    // Check if searched text is not blank
    if (text) {
      // Inserted text is not blank
      // Filter the masterDataSource and update FilteredDataSource
      const newData = parkings.filter(function (item) {
        // Applying filter for the inserted text in search bar
        const itemData = item.id
          ? item.id.toUpperCase()
          : ''.toUpperCase();
        const textData = text.toUpperCase();
        return itemData.indexOf(textData) > -1;
      });
      setFilteredDataSource(newData);
      setSearch(text);
    } else {
      // Inserted text is blank
      // Update FilteredDataSource with masterDataSource
      setFilteredDataSource(parkings);
      setSearch(text);
    }
  };

  const bottomSheetModalRef = useRef(null);
  const snapPoints = useMemo(() => ["40%"], []);
 
  const openModal = () => {
      bottomSheetModalRef.current.present();
    };

  const [search, setSearch] = useState('');
  const [filteredDataSource, setFilteredDataSource] = useState<LocationCoordProps[]>(parkings);


  return (
    <GestureHandlerRootView style={{flex: 1}}> 
      <BottomSheetModalProvider>
        <View style={styles.container}>
          <Map markers={parkings} />
          <View style={styles.searchContainer}>
            <TextInput
                  style={styles.textInputStyle}
                  onChangeText={(text) => searchFilterFunction(text)}
                  value={search}
                  onTouchStart={openModal}
                  underlineColorAndroid="transparent"
                  placeholder="Search Destinations"
                />
              <BottomSheetModal
                ref={bottomSheetModalRef}
                index={0}
                snapPoints={snapPoints}
                enablePanDownToClose={true}
              >
                <TextInput
                  style={styles.textInputStyle}
                  onChangeText={(text) => searchFilterFunction(text)}
                  value={search}
                  underlineColorAndroid="transparent"
                  placeholder="Search Destinations"
                />
                <FlatList
                  data={filteredDataSource}
                  keyExtractor={(item, index) => index.toString()}
                  ItemSeparatorComponent={ItemSeparatorView}
                  renderItem={ItemView}
                  keyboardShouldPersistTaps="always" // Manter o teclado aberto ao tocar na lista
                  onTouchStart={() => Keyboard.dismiss()} // Fechar o teclado quando tocar na lista
                />
              </BottomSheetModal>
          </View>
        </View>
      </BottomSheetModalProvider>
    </GestureHandlerRootView>
  );
}