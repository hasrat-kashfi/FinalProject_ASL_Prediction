import React, { useState } from 'react';
import { SafeAreaView,View, Text, TouchableOpacity, StyleSheet, Image } from 'react-native';

export default function App() {
  const [isButtonPressed, setIsButtonPressed] = useState(false);

  const handleButtonPress = () => {
    setIsButtonPressed(true);
    console.log('Button pressed:', isButtonPressed);
  };

  return (
    <SafeAreaView style={styles.container}>
      <View style={[styles.header, isButtonPressed && styles.headerPressed]}>
        <Text style={styles.headerText}>Final Project</Text>
        <Text style={styles.headerSubtext}>(Showcase)</Text>
      </View>
      <View style={styles.contentContainer}>
        <Image source={require('./assets/HS.png')} style={styles.image} />
        <View style={styles.buttonContainer}>
          <TouchableOpacity
            style={[styles.button, isButtonPressed && styles.buttonPressed]}
            onPress={() => {
              handleButtonPress();
              console.log('Button pressed:', true);
            }}
          >
            <View style={styles.icon}>
              <View style={styles.hand} />
            </View>
          </TouchableOpacity>
          <Text style={styles.buttonText}>
            Press Button to turn on{'\n'}Video to Text
          </Text>
        </View>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#121212',
    alignItems: 'center',
  },
  header: {
    backgroundColor: '#f2f2f2',
    width: '100%',
    paddingVertical: 16,
    paddingHorizontal: 24,
    borderBottomLeftRadius: 16,
    borderBottomRightRadius: 16,
    alignItems: 'center',
    
  },
  headerPressed: {
    backgroundColor: '#333',
    
  },
  headerText: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#121212',
  },
  headerSubtext: {
    fontSize: 16,
    color: '#666',
  },
  contentContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  image: {
    width: '80%',
    height: '40%',
    resizeMode: 'contain',
    marginBottom: 32,
  },
  buttonContainer: {
    alignItems: 'center',
  },
  button: {
    backgroundColor: '#f2f2f2',
    padding: 16,
    borderRadius: 24,
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
    elevation: 5,
  },
  buttonPressed: {
    backgroundColor: '#333',
  },
  buttonText: {
    fontSize: 16,
    color: '#121212',
    textAlign: 'center',
    marginTop: 8,
  },
  icon: {
    width: 48,
    height: 48,
    borderRadius: 24,
    backgroundColor: '#333',
    justifyContent: 'center',
    alignItems: 'center',
  },
  hand: {
    width: 24,
    height: 24,
    backgroundColor: '#f2f2f2',
    borderRadius: 12,
  },
});