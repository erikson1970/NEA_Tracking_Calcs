classdef SMAEdge_SamtecCustom < PCBConnectors.BaseSMT5PadEdge
    % Samtec SMA edge-launch surface mount RF connector.
    
    properties (Constant) % Abstract
        Type       = 'SMAEdge'
        Mfg        = 'Samtec'
        Part       = 'SMA-J-P-X-ST-EM1'
        Annotation = 'SMA'
        Impedance  = 50
        Datasheet  = 'http://suddendocs.samtec.com/prints/sma-j-p-x-st-em1-mkt.pdf'
        Purchase   = 'https://www.digikey.com/product-detail/en/samtec-inc/SMA-J-P-H-ST-EM1/SAM8857-ND/2602450'
    end
    
    methods
        function RFC = SMAEdge_SamtecCustom
            RFC.GroundPadSize      = [1.35e-3 4.2e-3];
            RFC.GroundSeparation   = 4.3e-3;
            RFC.GroundPadIsolation = 0.25e-3;
            RFC.SignalPadSize      = [1.27e-3 3.7e-3];
            RFC.SignalGap          = 0.1e-3;
            RFC.SignalLineWidth    = 1.5e-3;
            % Do not set RFC.EdgeLocation, leave it to caller.            
        end
    end
    
end


