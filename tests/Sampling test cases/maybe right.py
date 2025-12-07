def interpolateSignal(signal: SignalData, L: int) -> SignalData:
    """Interpolate a signal by factor L (upsampling with zero insertion)"""
    if signal.SignalType:
        raise ValueError("Interpolation is only implemented for time domain signals")
    
    # Get time domain data
    indices = sorted(signal.data.keys())
    amplitudes = [signal.data[idx] for idx in indices]
    
    # Upsample by inserting L-1 zeros between samples
    upsampled_indices = []
    upsampled_amplitudes = []
    
    for i, (idx, amp) in enumerate(zip(indices, amplitudes)):
        upsampled_indices.append(idx * L)
        upsampled_amplitudes.append(amp)
        
        # Insert zeros
        if i < len(indices) - 1:
            for j in range(1, L):
                upsampled_indices.append(idx * L + j)
                upsampled_amplitudes.append(0.0)
    
    # Create new SignalData object
    result = SignalData()
    result.SignalType = False  # Time domain
    result.IsPeriodic = signal.IsPeriodic
    result.N1 = len(upsampled_indices)
    result.data = {idx: amp for idx, amp in zip(upsampled_indices, upsampled_amplitudes)}
    
    return result


def decimateSignal(signal: SignalData, M: int) -> SignalData:
    """Decimate a signal by factor M (downsampling)"""
    if signal.SignalType:
        raise ValueError("Decimation is only implemented for time domain signals")
    
    # Get time domain data
    indices = sorted(signal.data.keys())
    amplitudes = [signal.data[idx] for idx in indices]
    
    # Downsample by taking every M-th sample
    downsampled_indices = []
    downsampled_amplitudes = []
    
    for i, (idx, amp) in enumerate(zip(indices, amplitudes)):
        if idx % M == 0:
            downsampled_indices.append(idx // M)
            downsampled_amplitudes.append(amp)
    
    # Create new SignalData object
    result = SignalData()
    result.SignalType = False  # Time domain
    result.IsPeriodic = signal.IsPeriodic
    result.N1 = len(downsampled_indices)
    result.data = {idx: amp for idx, amp in zip(downsampled_indices, downsampled_amplitudes)}
    
    return result


def applyFIRFilter(signal: SignalData, filter_coeff: np.ndarray) -> SignalData:
    """Apply FIR filter to a time domain signal"""
    if signal.SignalType:
        raise ValueError("FIR filtering is only implemented for time domain signals")
    
    # Get time domain data
    indices = sorted(signal.data.keys())
    amplitudes = [signal.data[idx] for idx in indices]
    
    # Apply FIR filter (convolution)
    filtered = np.convolve(amplitudes, filter_coeff, mode='same')
    
    # Create new SignalData object
    result = SignalData()
    result.SignalType = False  # Time domain
    result.IsPeriodic = signal.IsPeriodic
    result.N1 = len(indices)
    result.data = {idx: amp for idx, amp in zip(indices, filtered)}
    
    return result


def resampleSignal(signal_file: str, filter_spec_file: str, L: int, M: int) -> SignalData:
    """
    Resample a signal using interpolation factor L and decimation factor M
    with appropriate low-pass filtering.
    """
    # Read filter specifications
    filter_spec = readFilter(filter_spec_file)
    
    # Check if filter type is low pass
    if filter_spec.filterType != FilterType.LOW:
        print("Warning: Filter type is not low pass. Using low pass filtering anyway.")
    
    # Read signal data
    signal = readSignalData(signal_file)
    
    # If signal is in frequency domain, convert to time domain
    # (This is a simplified conversion - for actual use, implement proper IDFT)
    if signal.SignalType:
        print("Warning: Frequency domain signals need proper IDFT implementation")
        # For simplicity, we'll create a dummy time domain signal
        # In practice, you would implement an inverse Fourier transform here
        time_signal = SignalData()
        time_signal.SignalType = False
        time_signal.IsPeriodic = signal.IsPeriodic
        time_signal.N1 = signal.N1
        time_signal.data = {i: 0.0 for i in range(signal.N1)}
        signal = time_signal
    
    # Step 1: Interpolate (upsample) by factor L
    if L > 1:
        upsampled_signal = interpolateSignal(signal, L)
        
        # Step 2: Design and apply anti-imaging low-pass filter
        # The cutoff should be at the original Nyquist frequency
        anti_imaging_filter = designLowPassFilter(filter_spec, L)
        filtered_signal = applyFIRFilter(upsampled_signal, anti_imaging_filter)
    else:
        filtered_signal = signal
    
    # Step 3: Decimate (downsample) by factor M
    if M > 1:
        # Before decimating, we need to apply an anti-aliasing filter
        # with cutoff at Fs/(2M) where Fs is the current sampling rate
        current_Fs = filter_spec.FS * (L if L > 1 else 1)
        filter_spec.FC = current_Fs / (2 * M)  # Adjust cutoff for anti-aliasing
        
        anti_aliasing_filter = designLowPassFilter(filter_spec, 1)
        filtered_signal = applyFIRFilter(filtered_signal, anti_aliasing_filter)
        
        resampled_signal = decimateSignal(filtered_signal, M)
    else:
        resampled_signal = filtered_signal
    
    return resampled_signal